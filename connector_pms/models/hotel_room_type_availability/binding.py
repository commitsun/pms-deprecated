# Copyright 2018-2019 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import timedelta

from odoo.addons.queue_job.job import job

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


class ChannelHotelRoomTypeAvailability(models.Model):
    _name = "channel.hotel.room.type.availability"
    _inherit = "channel.binding"
    _inherits = {"hotel.room.type.availability": "odoo_id"}
    _description = "Channel Availability"

    odoo_id = fields.Many2one(
        comodel_name="hotel.room.type.availability", required=True, ondelete="cascade"
    )
    channel_avail = fields.Integer(
        "Availability",
        readonly=True,
        track_visibility="always",
        help="Availability of the room type for the channel manager."
        "This availability is set based on the real availability, "
        "the quota, and the max availability.",
    )
    channel_pushed = fields.Boolean(
        "Channel Pushed", readonly=True, default=False)

    @api.model
    def refresh_availability(
        self,
        checkin,
        checkout,
        backend_id,
        room_id=False,
        room_type_id=False,
        from_channel=False,
    ):
        date_start = checkin
        date_end = checkout
        if date_start == date_end:
            date_end = date_start + timedelta(days=1)
        # Not count end day of the reservation
        date_diff = (date_end - date_start).days

        channel_room_type_obj = self.env["channel.hotel.room.type"]
        channel_room_type_avail_obj = self.env["channel.hotel.room.type.availability"]
        if room_type_id:
            room_type_bind = channel_room_type_obj.search(
                [("odoo_id", "=", room_type_id)]
            )
        else:
            domain = [("backend_id", "=", backend_id)]
            if room_id:
                domain.append(("room_ids", "in", [room_id]))
                # WARNING: more than one binding is currently not expected
            room_type_bind = channel_room_type_obj.search(domain, limit=1)
        if room_type_bind and room_type_bind.external_id:
            _logger.info("==[ODOO->CHANNEL]==== REFRESH AVAILABILITY ==")
            for i in range(0, date_diff):
                ndate_dt = date_start + timedelta(days=i)
                ndate_str = ndate_dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                to_eval = []
                # real availability based on rooms
                cavail = len(
                    channel_room_type_obj.odoo_id.check_availability_room_type(
                        ndate_str, ndate_str, room_type_id=room_type_bind.odoo_id.id
                    )
                )
                to_eval.append(cavail)

                room_type_avail_id = channel_room_type_avail_obj.search(
                    [
                        ("room_type_id", "=", room_type_bind.odoo_id.id),
                        ("date", "=", ndate_str),
                    ],
                    limit=1,
                )

                quota = (
                    room_type_avail_id.quota
                    if room_type_avail_id
                    else room_type_bind.default_quota
                )
                max_avail = (
                    room_type_avail_id.max_avail
                    if room_type_avail_id
                    else room_type_bind.default_max_avail
                )

                if from_channel and quota > 0:
                    quota -= 1
                # We ignore quota and max_avail if its value is -1
                if quota >= 0:
                    to_eval.append(quota)
                if max_avail >= 0:
                    to_eval.append(max_avail)
                # And finally, set the channel avail like the min set value
                avail = max(min(to_eval), 0)

                if room_type_avail_id:
                    # CAVEAT: update channel.hotel.room.type.availability if
                    # needed
                    vals_avail = {}
                    if room_type_avail_id.quota != quota:
                        vals_avail.update({"quota": quota})
                        _logger.info(vals_avail)
                    if room_type_avail_id.channel_avail != avail:
                        vals_avail.update({"channel_avail": avail})
                    if self._context.get("update_no_ota", False) or from_channel:
                        vals_avail.update({"channel_pushed": False})
                    if vals_avail:
                        room_type_avail_id.write(vals_avail)

                    # Auto-Fix channel quota and max availability
                    # vals_avail = {}
                    # # TODO: reduce quota by one instead of adjust to
                    #  current channel availability
                    # if room_type_avail_id.quota > avail:
                    #     vals_avail.update({'quota': avail})
                    #     _logger.info(vals_avail)
                    # if room_type_avail_id.max_avail > avail:
                    #     vals_avail.update({'max_avail': avail})
                    # if vals_avail:
                    #     room_type_avail_id.with_context(
                    #     {'connector_no_export': True}
                    # ).write(vals_avail)
                else:
                    self.env["hotel.room.type.availability"].with_context(
                        {"connector_no_export": True}
                    ).create(
                        {
                            "room_type_id": room_type_bind.odoo_id.id,
                            "date": ndate_str,
                            "quota": quota,
                            "channel_bind_ids": [
                                (
                                    0,
                                    False,
                                    {
                                        "channel_avail": avail,
                                        "channel_pushed": False,
                                        "backend_id": backend_id,
                                    },
                                )
                            ],
                        }
                    )
            self.push_availability(
                self.env["channel.backend"].browse(backend_id))

    @job(default_channel="root.channel")
    @api.model
    def import_availability(self, backend, dfrom, dto):
        with backend.work_on(self._name) as work:
            importer = work.component(
                usage="hotel.room.type.availability.importer")
            return importer.import_availability_values(dfrom, dto)

    @job(default_channel="root.channel")
    @api.model
    def push_availability(self, backend):
        with backend.work_on(self._name) as work:
            exporter = work.component(
                usage="hotel.room.type.availability.exporter")
            return exporter.push_availability()
