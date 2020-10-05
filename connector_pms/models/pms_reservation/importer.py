# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsReservationImporter(Component):
    _name = "channel.pms.reservation.importer"
    _inherit = "pms.channel.importer"
    _apply_on = ["channel.pms.reservation"]
    _usage = "pms.reservation.importer"

    @api.model
    def fetch_booking(self, channel_reservation_id):
        raise NotImplementedError

    def fetch_new_bookings(self):
        raise NotImplementedError

    def fetch_bookings(self, dfrom, dto):
        raise NotImplementedError
