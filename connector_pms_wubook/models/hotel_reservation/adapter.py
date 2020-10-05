# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class HotelReservationAdapter(Component):
    _name = "channel.hotel.reservation.adapter"
    _inherit = "wubook.adapter"
    _apply_on = "channel.hotel.reservation"

    def mark_bookings(self, channel_reservation_ids):
        return super(HotelReservationAdapter, self).mark_bookings(
            channel_reservation_ids
        )

    def fetch_new_bookings(self):
        return super(HotelReservationAdapter, self).fetch_new_bookings()

    def fetch_bookings(self, dfrom, dto):
        return super(HotelReservationAdapter, self).fetch_bookings(dfrom, dto)

    def fetch_booking(self, channel_reservation_id):
        return super(HotelReservationAdapter, self).fetch_booking(
            channel_reservation_id
        )

    def cancel_reservation(self, channel_reservation_id, message):
        return super(HotelReservationAdapter, self).cancel_reservation(
            channel_reservation_id, message
        )
