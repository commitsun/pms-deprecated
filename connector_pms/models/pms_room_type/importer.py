# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeImporter(Component):
    _name = "channel.pms.room.type.importer"
    _inherit = "pms.channel.importer"
    _apply_on = ["channel.pms.room.type"]
    _usage = "pms.room.type.importer"

    @api.model
    def get_rooms(self):
        raise NotImplementedError
