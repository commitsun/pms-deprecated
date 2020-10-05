# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.queue_job.job import job

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChannelHotelReservation(models.Model):
    _name = "channel.hotel.reservation"
    _inherit = "channel.binding"
    _inherits = {"hotel.reservation": "odoo_id"}
    _description = "Channel Hotel Reservation"

    odoo_id = fields.Many2one(
        comodel_name="hotel.reservation",
        string="Reservation",
        required=True,
        ondelete="cascade",
    )
    ota_id = fields.Many2one(
        "channel.ota.info", string="Channel OTA ID", readonly=True)
    ota_reservation_id = fields.Char(
        "Channel OTA Reservation Code", readonly=True)
    channel_raw_data = fields.Text(readonly=True)

    channel_status = fields.Selection(
        [("0", "No Channel")], string="Channel Status", default="0", readonly=True
    )
    channel_status_reason = fields.Char("Channel Status Reason", readonly=True)
    channel_modified = fields.Boolean(
        "Channel Modified", readonly=True, default=False)

    channel_total_amount = fields.Monetary(
        string="Channel Total Amount", readonly=True, digits="Product Price"
    )

    # Inherit binding constrain becouse two reservations can have
    # the same external_id
    _sql_constraints = [
        (
            "channel_uniq",
            "unique(odoo_id, external_id)",
            "A binding already exists with the same Channel ID.",
        ),
    ]

    @job(default_channel="root.channel")
    @api.model
    def refresh_availability(
        self,
        checkin,
        checkout,
        backend_id,
        room_id,
        room_type_id=False,
        from_channel=False,
    ):
        self.env["channel.hotel.room.type.availability"].refresh_availability(
            checkin, checkout, backend_id, room_id, room_type_id, from_channel
        )

    @job(default_channel="root.channel")
    @api.model
    def import_reservation(self, backend, channel_reservation_id):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="hotel.reservation.importer")
            return importer.fetch_booking(channel_reservation_id)

    @job(default_channel="root.channel")
    @api.model
    def import_reservations(self, backend):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="hotel.reservation.importer")
            return importer.fetch_new_bookings()

    @job(default_channel="root.channel")
    @api.model
    def import_reservations_range(self, backend, dfrom, dto):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="hotel.reservation.importer")
            return importer.fetch_bookings(dfrom, dto)

    @job(default_channel="root.channel")
    def cancel_reservation(self):
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage="hotel.reservation.exporter")
            return exporter.cancel_reservation(self)

    @job(default_channel="root.channel")
    def mark_booking(self):
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage="hotel.reservation.exporter")
            return exporter.mark_booking(self)

    def unlink(self):
        vals = []
        for record in self:
            if record.is_from_ota and self._context.get("ota_limits", True):
                raise UserError(_("You can't delete OTA's reservations"))
            backend_id = (
                self.env["channel.hotel.room.type"]
                .search([("odoo_id", "=", record.room_id.room_type_id.id)])
                .backend_id.id
            )
            vals.append(
                {
                    "checkin": record.checkin,
                    "checkout": record.checkout,
                    "backend_id": backend_id,
                    "room_id": record.room_id.id,
                }
            )
        res = super(ChannelHotelReservation, self).unlink()
        if self._context.get("connector_no_export", True):
            channel_room_type_avail_obj = self.env[
                "channel.hotel.room.type.availability"
            ]
            for record in vals:
                # FIX: 3rd parameters is backend_id, use room_id=record[
                # 'room_id'] instead
                channel_room_type_avail_obj.sudo().refresh_availability(
                    record["checkin"],
                    record["checkout"],
                    record["backend_id"],
                    record["room_id"],
                )
        return res
