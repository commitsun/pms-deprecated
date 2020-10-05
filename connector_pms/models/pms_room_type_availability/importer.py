# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeAvailabilityImporter(Component):
    _name = "channel.pms.room.type.availability.importer"
    _inherit = "pms.channel.importer"
    _apply_on = ["channel.pms.room.type.availability"]
    _usage = "pms.room.type.availability.importer"

    @api.model
    def import_availability_values(self, date_from, date_to):
        raise NotImplementedError
