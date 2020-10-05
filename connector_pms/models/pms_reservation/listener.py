# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class ChannelBindingPmsReservationListener(Component):
    _name = "channel.binding.pms.reservation.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.pms.reservation"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.refresh_availability()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = (
            "room_id",
            "state",
            "checkin",
            "checkout",
            "room_type_id",
            "reservation_line_ids",
            "splitted",
            "overbooking",
        )
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            record.refresh_availability()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_unlink(self, record, fields=None):
        record.refresh_availability()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_cancel(self, record, fields=None):
        record.cancel_reservation()
