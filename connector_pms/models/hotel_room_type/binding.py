# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.job import job


class ChannelHotelRoomType(models.Model):
    _name = "channel.hotel.room.type"
    _inherit = "channel.binding"
    _inherits = {"hotel.room.type": "odoo_id"}
    _description = "Channel Hotel Room"

    @api.model
    def _default_max_avail(self):
        return (
            self.env["hotel.room.type"]
            .browse(self._context.get("default_odoo_id"))
            .total_rooms_count
            or -1
        )

    @api.model
    def _default_availability(self):
        return max(min(self.default_quota, self.default_max_avail), 0)

    odoo_id = fields.Many2one(
        comodel_name="hotel.room.type",
        string="Room Type",
        required=True,
        ondelete="cascade",
    )
    channel_short_code = fields.Char("Channel Short Code")
    ota_capacity = fields.Integer(
        "OTA's Capacity", default=1, help="The capacity of the room for OTAs."
    )

    default_quota = fields.Integer(
        "Default Quota",
        help="Quota assigned to the channel given no availability rules. "
        "Use `-1` for managing no quota.",
    )
    default_max_avail = fields.Integer(
        "Max. Availability",
        default=_default_max_avail,
        help="Maximum simultaneous availability given no availability rules. "
        "Use `-1` for using maximum simultaneous availability.",
    )
    default_availability = fields.Integer(
        default=_default_availability,
        readonly=True,
        help="Default availability for OTAs. "
        "The availability is calculated based on the quota, "
        "the maximum simultaneous availability and "
        "the total room count for the given room type.",
    )

    min_price = fields.Float(
        "Min. Price",
        default=5.0,
        digits="Product Price",
        help="Setup the min price to prevent incidents while editing your " "prices.",
    )
    max_price = fields.Float(
        "Max. Price",
        default=200.0,
        digits="Product Price",
        help="Setup the max price to prevent incidents while editing your " "prices.",
    )

    @api.constrains("default_quota", "default_max_avail", "total_rooms_count")
    def _constrains_availability(self):
        for rec in self:
            to_eval = []
            to_eval.append(rec.total_rooms_count)
            if rec.default_quota >= 0:
                to_eval.append(rec.default_quota)
            if rec.default_max_avail >= 0:
                to_eval.append(rec.default_max_avail)

            rec.default_availability = min(to_eval)

    @api.constrains("room_ids")
    def _constrain_capacity(self):
        for rec in self:
            rec.ota_capacity = rec.odoo_id.get_capacity()

    def _check_self_unlink(self):
        if not self.odoo_id:
            self.sudo().unlink()

    @job(default_channel="root.channel")
    @api.model
    def import_rooms(self, backend):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="hotel.room.type.importer")
            return importer.get_rooms()

    @api.constrains("ota_capacity")
    def _check_ota_capacity(self):
        for record in self:
            if record.ota_capacity < 1:
                raise ValidationError(_("OTA's capacity can't be less than one"))
            if record.ota_capacity > record.capacity:
                raise ValidationError(
                    _("OTA's capacity can't be greater than room type capacity")
                )

    @api.constrains("channel_short_code")
    def _check_channel_short_code(self):
        for record in self:
            # Wubook scode max. length
            if self.channel_short_code and len(record.channel_short_code) > 4:
                raise ValidationError(
                    _("Chanel short code can't be longer than 4 characters")
                )

    @job(default_channel="root.channel")
    def create_room(self):
        self.ensure_one()
        if not self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="hotel.room.type.exporter")
                exporter.create_room(self)

    @job(default_channel="root.channel")
    def modify_room(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="hotel.room.type.exporter")
                exporter.modify_room(self)

    @job(default_channel="root.channel")
    def delete_room(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                deleter = work.component(usage="hotel.room.type.deleter")
                deleter.delete_room(self)
