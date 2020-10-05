# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ChannelHotelRoomType(models.Model):
    _inherit = "channel.hotel.room.type"

    @api.constrains("min_price", "max_price")
    def _check_min_max_price(self):
        for record in self:
            if record.min_price < 5 or record.max_price < 5:
                msg = _(
                    "The channel manager limits the minimum value of min "
                    "price and max price to 5."
                )
                raise ValidationError(msg)
