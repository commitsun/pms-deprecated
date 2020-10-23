# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime

import pytz

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ChannelWubookProductPricelistItemMapperImport(Component):
    _name = "channel.wubook.product.pricelist.item.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.product.pricelist.item"

    @mapping
    def items(self, record):
        def to_naive_utc(dt):
            dt = datetime.datetime(*dt.timetuple()[:3])
            dt = pytz.timezone(pms_property_id.tz).localize(dt)
            dt = dt.astimezone(pytz.utc)
            dt = dt.replace(tzinfo=None)
            return dt

        pms_property_id = self.backend_record.pms_property_id
        ttype = record["type"]
        if ttype == "pricelist":
            pl_binder = self.binder_for("channel.wubook.product.pricelist")
            pricelist = pl_binder.to_internal(record["vpid"], unwrap=True)
            if not pricelist:
                raise ValidationError(
                    _(
                        "External record with id %i not exists. "
                        "It should be imported in _import_dependencies"
                    )
                    % record["vpid"]
                )
            values = {
                "applied_on": "3_global",
                "compute_price": "formula",
                "base": "pricelist",
                "base_pricelist_id": pricelist.id,
                "pms_property_ids": [(6, 0, pms_property_id.ids)],
            }

            variation_type = record["variation_type"]
            variation = record["variation"]
            if variation_type == -2:
                values["price_discount"] = 0
                values["price_surcharge"] = -variation
            elif variation_type == -1:
                values["price_discount"] = variation
                values["price_surcharge"] = 0
            elif variation_type == 1:
                values["price_discount"] = -variation
                values["price_surcharge"] = 0
            elif variation_type == 2:
                values["price_discount"] = 0
                values["price_surcharge"] = variation
            else:
                raise ValidationError(_("Unknown variation type %s") % variation_type)
        elif ttype == "room":
            rt_binder = self.binder_for("channel.wubook.pms.room.type")
            room_type = rt_binder.to_internal(record["rid"], unwrap=True)
            if not room_type:
                raise ValidationError(
                    _(
                        "External record with id %i not exists. "
                        "It should be imported in _import_dependencies"
                    )
                    % record["rid"]
                )

            values = {
                "applied_on": "0_product_variant",
                "compute_price": "fixed",
                "product_id": room_type.product_id.id,
                "fixed_price": record["price"],
                "date_start": to_naive_utc(record["date"]),
                "date_end": to_naive_utc(record["date"]),
                "pms_property_ids": [(6, 0, pms_property_id.ids)],
            }
        else:
            raise ValidationError(_("Unknown type '%s'") % ttype)

        return values
