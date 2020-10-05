# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.product.pricelist.item",
        inverse_name="odoo_id",
        string="Pms Channel Connector Bindings",
    )

    @api.constrains("fixed_price")
    def _check_fixed_price(self):
        for record in self:
            channel_room_type = self.env["channel.pms.room.type"].search(
                [("product_tmpl_id", "=", record.product_tmpl_id.id)]
            )
            if channel_room_type and (
                record.fixed_price < channel_room_type.min_price
                or record.fixed_price > channel_room_type.max_price
            ):
                msg = _(
                    "The room type '%s' limits the price between '%s' and '%s'."
                ) % (
                    record.name,
                    channel_room_type.min_price,
                    channel_room_type.max_price,
                )
                raise ValidationError(msg)
