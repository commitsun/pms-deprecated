# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeRestrictionDeleter(Component):
    _name = "channel.pms.room.type.restriction.deleter"
    _inherit = "pms.channel.deleter"
    _apply_on = ["channel.pms.room.type.restriction"]
    _usage = "pms.room.type.restriction.deleter"

    @api.model
    def delete_rplan(self, binding):
        raise NotImplementedError
