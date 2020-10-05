# Copyright 2018-2019 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HotelRoomTypeAvailability(models.Model):
    _name = "hotel.room.type.availability"
    _inherit = "mail.thread"

    @api.model
    def _default_max_avail(self):
        room_type_id = self.room_type_id.id or self._context.get("room_type_id")
        channel_room_type = (
            self.env["channel.hotel.room.type"].search(
                [("odoo_id", "=", room_type_id)])
            or None
        )
        if channel_room_type:
            return channel_room_type.default_max_avail
        return -1

    @api.model
    def _default_quota(self):
        room_type_id = self.room_type_id.id or self._context.get("room_type_id")
        channel_room_type = (
            self.env["channel.hotel.room.type"].search(
                [("odoo_id", "=", room_type_id)])
            or None
        )
        if channel_room_type:
            return channel_room_type.default_quota
        return -1

    room_type_id = fields.Many2one(
        "hotel.room.type", "Room Type", required=True, tracking=True, ondelete="cascade"
    )
    channel_bind_ids = fields.One2many(
        comodel_name="channel.hotel.room.type.availability",
        inverse_name="odoo_id",
        string="Hotel Room Type Availability Connector Bindings",
    )

    date = fields.Date("Date", required=True, track_visibility="always")

    quota = fields.Integer(
        "Quota",
        default=_default_quota,
        tracking=True,
        help="Quota assigned to the channel.",
    )
    # TODO: WHY max_avail IS READONLY ¿?
    max_avail = fields.Integer(
        "Max. Availability",
        default=-1,
        readonly=True,
        track_visibility="always",
        help="Maximum simultaneous availability.",
    )

    no_ota = fields.Boolean(
        "No OTA",
        default=False,
        tracking=True,
        help="Set zero availability to the connected OTAs "
        "even when the availability is positive,"
        "except to the Online Reception (booking engine)",
    )
    booked = fields.Boolean("Booked", default=False, readonly=True)

    _sql_constraints = [
        (
            "room_type_registry_unique",
            "unique(room_type_id, date)",
            "Only can exists one availability in the same day for the same "
            "room \
          type!",
        )
    ]

    @api.onchange("room_type_id")
    def onchange_room_type_id(self):
        channel_room_type = (
            self.env["channel.hotel.room.type"].search(
                [("odoo_id", "=", self.room_type_id.id)]
            )
            or None
        )
        if channel_room_type:
            self.quota = channel_room_type.default_quota
            self.max_avail = channel_room_type.default_max_avail
            self.no_ota = 0

    @api.model
    def create(self, vals):
        vals.update(self._prepare_add_missing_fields(vals))
        return super().create(vals)

    @api.model
    def _prepare_add_missing_fields(self, values):
        """ Deduce missing required fields from the onchange """
        res = {}
        onchange_fields = ["quota", "max_avail"]
        if values.get("room_type_id"):
            record = self.new(values)
            if "quota" not in values:
                record.quota = record._default_quota()
            if "max_avail" not in values:
                record.max_avail = record._default_max_avail()
            for field in onchange_fields:
                if field not in values:
                    res[field] = record._fields[field].convert_to_write(
                        record[field], record
                    )
        return res
