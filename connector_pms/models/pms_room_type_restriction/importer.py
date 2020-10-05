# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeRestrictionImporter(Component):
    _name = "channel.pms.room.type.restriction.importer"
    _inherit = "pms.channel.importer"
    _apply_on = ["channel.pms.room.type.restriction"]
    _usage = "pms.room.type.restriction.importer"

    @api.model
    def import_restriction_plans(self):
        raise NotImplementedError
