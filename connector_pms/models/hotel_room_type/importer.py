# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class HotelRoomTypeImporter(Component):
    _name = "channel.hotel.room.type.importer"
    _inherit = "hotel.channel.importer"
    _apply_on = ["channel.hotel.room.type"]
    _usage = "hotel.room.type.importer"

    @api.model
    def get_rooms(self):
        raise NotImplementedError
