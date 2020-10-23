# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ChannelWubookPmsAvailabilityPlanRuleMapperImport(Component):
    _name = "channel.wubook.pms.availability.plan.rule.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.pms.availability.plan.rule"

    @mapping
    def items(self, record):
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
            # TODO
            pass
        else:
            raise ValidationError(_("Unknown type '%s'") % ttype)

        return values
