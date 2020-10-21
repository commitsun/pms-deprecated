# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class HotelRoomTypeRestrictionImporter(Component):
    _name = "channel.hotel.room.type.restriction.importer"
    _inherit = "hotel.channel.importer"
    _apply_on = ["channel.hotel.room.type.restriction"]
    _usage = "hotel.room.type.restriction.importer"

    @api.model
    def import_restriction_plans(self):
        raise NotImplementedError
