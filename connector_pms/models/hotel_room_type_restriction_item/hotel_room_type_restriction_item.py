# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HotelRoomTypeRestrictionItem(models.Model):
    _inherit = "hotel.room.type.restriction.item"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.hotel.room.type.restriction.item",
        inverse_name="odoo_id",
        string="Hotel Channel Connector Bindings",
    )
