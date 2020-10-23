# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class ChannelWubookPmsFolioMapperImport(Component):
    _name = "channel.wubook.pms.folio.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.pms.folio"

    direct = [
        # ("men", "adults"),
        # ("children", "children"),
    ]

    children = [
        ("reservations", "reservation_ids", "channel.wubook.pms.reservation"),
    ]

    @only_create
    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @only_create
    @mapping
    def property_id(self, record):
        return {"pms_property_id": self.backend_record.pms_property_id.id}

    @only_create
    @mapping
    def pricelist_id(self, record):
        pricelist_id = False
        if record["rate_id"]:
            binder = self.binder_for("channel.wubook.product.pricelist")
            pricelist = binder.to_internal(record["rate_id"], unwrap=True)
            assert pricelist, (
                "rate_id %s should have been imported in "
                "ProductPricelistImporter._import_dependencies" % (record["rate_id"],)
            )
            pricelist_id = pricelist.id
        # TODO:
        if pricelist_id:
            return {"pricelist_id": pricelist_id}

    @only_create
    @mapping
    def partner_id(self, record):
        values = {
            "name": "{}, {}".format(
                record["customer_surname"], record["customer_name"]
            ),
            "city": record["customer_city"],
            "phone": record["customer_phone"],
            "zip": record["customer_zip"],
            "street": record["customer_address"],
            "email": record["customer_mail"],
        }
        country = self.env["res.country"].search(
            [("code", "=", record["customer_country"])], limit=1
        )
        if country:
            values["country_id"] = (country.id,)
        lang = self.env["res.lang"].search(
            [("code", "=", record["customer_language_iso"])], limit=1
        )
        if lang:
            values["lang"] = lang.id
        partner = self.env["res.partner"].create(values)
        return {"partner_id": partner.id}


class ChannelWubookPmsFolioChildMapperImport(Component):
    _name = "channel.wubook.pms.folio.child.mapper.import"
    _inherit = "channel.wubook.child.mapper.import"
    _apply_on = "channel.wubook.pms.reservation"

    def get_item_values(self, map_record, to_attr, options):
        values = super().get_item_values(map_record, to_attr, options)
        binding = options.get("binding")
        if binding:
            # TODO heuristic to decide how to update existing reservations
            pass
        else:
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
