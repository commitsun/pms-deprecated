# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeDeleter(Component):
    _name = "channel.pms.room.type.deleter"
    _inherit = "pms.channel.deleter"
    _apply_on = ["channel.pms.room.type"]
    _usage = "pms.room.type.deleter"

    @api.model
    def delete_room(self, binding):
        raise NotImplementedError
