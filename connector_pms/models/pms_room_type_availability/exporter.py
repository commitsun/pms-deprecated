# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class PmsRoomTypeAvailabilityExporter(Component):
    _name = "channel.pms.room.type.availability.exporter"
    _inherit = "pms.channel.exporter"
    _apply_on = ["channel.pms.room.type.availability"]
    _usage = "pms.room.type.availability.exporter"

    def push_availability(self):
        raise NotImplementedError
