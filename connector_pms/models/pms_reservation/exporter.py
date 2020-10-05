# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsReservationExporter(Component):
    _name = "channel.pms.reservation.exporter"
    _inherit = "pms.channel.exporter"
    _apply_on = ["channel.pms.reservation"]
    _usage = "pms.reservation.exporter"

    @api.model
    def cancel_reservation(self, binding):
        raise NotImplementedError

    @api.model
    def mark_booking(self, binding):
        raise NotImplementedError

    @api.model
    def mark_bookings(self, external_ids):
        raise NotImplementedError
