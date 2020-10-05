# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeExporter(Component):
    _name = "channel.pms.room.type.exporter"
    _inherit = "pms.channel.exporter"
    _apply_on = ["channel.pms.room.type"]
    _usage = "pms.room.type.exporter"

    @api.model
    def modify_room(self, binding):
        raise NotImplementedError

    @api.model
    def create_room(self, binding):
        raise NotImplementedError
