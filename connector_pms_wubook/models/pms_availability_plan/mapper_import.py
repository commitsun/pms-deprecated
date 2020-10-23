# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class ChannelWubookPmsAvailabilityPlanMapperImport(Component):
    _name = "channel.wubook.pms.availability.plan.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.pms.availability.rule"

    direct = [
        ("name", "name"),
    ]

    children = [("items", "item_ids", "channel.wubook.pms.availability.plan.rule")]

    @only_create
    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def pricelist_type(self, record):
        return {"pricelist_type": "daily"}

    @mapping
    def property_ids(self, record):
        return {"pms_property_ids": [(6, 0, [self.backend_record.pms_property_id.id])]}


class ChannelWubookPmsAvailabilityPlanChildMapperImport(Component):
    _name = "channel.wubook.pms.availability.plan.child.mapper.import"
    _inherit = "channel.wubook.child.mapper.import"
    _apply_on = "channel.wubook.pms.availability.plan.rule"

    def get_item_values(self, map_record, to_attr, options):
        values = super().get_item_values(map_record, to_attr, options)
        common_keys = {"applied_on", "compute_price"}
        if {*common_keys, "base", "base_pricelist_id"}.issubset(values):
            binding = options.get("binding")
            if binding:
                item_ids = binding.item_ids.filtered(
                    lambda x: all(
                        [
                            x.applied_on == values["applied_on"],
                            x.compute_price == values["compute_price"],
                            x.base == values["base"],
                            x.base_pricelist_id.id == values["base_pricelist_id"],
                        ]
                    )
                )
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
        for values in items_values:
            _id = values.pop("id", None)
            if _id:
                ops.append((1, _id, values))
            else:
                ops.append((0, 0, values))

        return ops
