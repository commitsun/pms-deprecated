# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.product.pricelist",
        inverse_name="odoo_id",
        string="Pms Channel Connector Bindings",
    )

    pricelist_type = fields.Selection(selection_add=[("virtual", "Virtual Plan")])

    @api.depends("item_ids")
    def _compute_virtual_plan(self):
        for record in self:
            record.is_virtual_plan = True
            if any(
                item.applied_on != "3_global"
                or (item.date_start or item.date_end)
                or item.compute_price != "formula"
                or item.base != "pricelist"
                or not item.base_pricelist_id.is_daily_plan
                or (item.price_discount != 0 and item.price_surcharge != 0)
                or item.min_quantity != 0
                or item.price_round != 0
                or item.price_min_margin != 0
                or item.price_max_margin != 0
                for item in record.item_ids
            ):
                record.is_virtual_plan = False

    @api.depends("name")
    def name_get(self):
        pricelist_obj = self.env["product.pricelist"]
        org_names = super(ProductPricelist, self).name_get()
        names = []
        for name in org_names:
            pricelist_id = pricelist_obj.browse(name[0])
            new_name = name[1]
            if any(pricelist_id.channel_bind_ids):
                for pricelist_bind in pricelist_id.channel_bind_ids:
                    if pricelist_bind.external_id:
                        new_name += " (%s Backend)" % pricelist_bind.backend_id.name
                names.append((name[0], new_name))
            else:
                names.append((name[0], name[1]))
        return names

    def open_channel_bind_ids(self):
        channel_bind_ids = self.mapped("channel_bind_ids")
        action = self.env.ref("connector_pms.channel_product_pricelist_action").read()[
            0
        ]
        action["views"] = [
            (
                self.env.ref("connector_pms.channel_product_pricelist_view_form").id,
                "form",
            )
        ]
        action["target"] = "new"
        if len(channel_bind_ids) == 1:
            action["res_id"] = channel_bind_ids.ids[0]
        elif len(channel_bind_ids) > 1:
            # WARNING: more than one binding is currently not expected
            action["domain"] = [("id", "in", channel_bind_ids.ids)]
        else:
            action["context"] = {
                "default_odoo_id": self.id,
                "default_name": self.name,
                "default_pricelist_plan": self.pricelist_type,
            }
        return action

    def disconnect_channel_bind_ids(self):
        # TODO: multichannel rooms is not implemented
        self.channel_bind_ids.with_context({"connector_no_export": True}).unlink()

    def write(self, vals):
        if "active" in vals and vals.get("active") is False:
            self.channel_bind_ids.unlink()
        return super().write(vals)
