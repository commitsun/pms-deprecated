# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeRestrictionExporter(Component):
    _name = "channel.pms.room.type.restriction.exporter"
    _inherit = "pms.channel.exporter"
    _apply_on = ["channel.pms.room.type.restriction"]
    _usage = "pms.room.type.restriction.exporter"

    @api.model
    def rename_rplan(self, binding):
        raise NotImplementedError

    @api.model
    def create_rplan(self, binding):
        raise NotImplementedError
