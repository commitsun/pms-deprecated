# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class ChannelWubookProductPricelistMapperImport(Component):
    _name = "channel.wubook.product.pricelist.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.product.pricelist"

    direct = [
        ("name", "name"),
    ]

    children = [("items", "item_ids", "channel.wubook.product.pricelist.item")]

    @only_create
    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def pricelist_type(self, record):
        return {"pricelist_type": "daily"}

    @mapping
    def pms_property_ids(self, record):
        return {"pms_property_ids": [(6, 0, [self.backend_record.pms_property_id.id])]}


class ChannelWubookProductPricelistChildMapperImport(Component):
    _name = "channel.wubook.product.pricelist.child.mapper.import"
    _inherit = "channel.wubook.child.mapper.import"
    _apply_on = "channel.wubook.product.pricelist.item"

    def get_item_values(self, map_record, to_attr, options):
        values = super().get_item_values(map_record, to_attr, options)
        binding = options.get("binding")
        if binding:
            applied_on = values.get("applied_on")
            if applied_on == "3_global":
                item_ids = binding.item_ids.filtered(
                    lambda x: all(
                        [
                            x.applied_on == applied_on,
                            x.compute_price == values["compute_price"],
                            x.base == values["base"],
                            x.base_pricelist_id.id == values["base_pricelist_id"],
                            set(x.pms_property_ids.ids)
                            == set(values["pms_property_ids"][0][2]),
                        ]
                    )
                )
            elif applied_on == "0_product_variant":
                item_ids = binding.item_ids.filtered(
                    lambda x: all(
                        [
                            x.applied_on == applied_on,
                            x.compute_price == values["compute_price"],
                            x.product_id.id == values["product_id"],
                            x.date_start == values["date_start"],
                            x.date_end == values["date_end"],
                            set(x.pms_property_ids.ids)
                            == set(values["pms_property_ids"][0][2]),
                        ]
                    )
                )
            else:
                raise ValidationError(_("Unexpected pricelist type '%s'") % applied_on)

            if item_ids:
                if len(item_ids) > 1:
                    raise ValidationError(
                        _(
                            "Found two pricelist items with same properties %s. "
                            "Please remove one of them"
                        )
                        % values
                    )
                values["id"] = item_ids.id

        return values

    def format_items(self, items_values):
        ops = []
        items_values = sorted(
            items_values, key=lambda x: (x["product_id"], x["date_start"]), reverse=True
        )
        for values in items_values:
            _id = values.pop("id", None)
            if _id:
                ops.append((1, _id, values))
            else:
                ops.append((0, 0, values))

        return ops
