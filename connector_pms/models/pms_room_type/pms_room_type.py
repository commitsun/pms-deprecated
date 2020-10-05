# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PmsRoomType(models.Model):
    _inherit = "pms.room.type"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.pms.room.type",
        inverse_name="odoo_id",
        string="Pms Channel Connector Bindings",
    )

    capacity = fields.Integer("Capacity", compute="_compute_capacity", store=True)

    @api.depends("room_ids")
    def _compute_capacity(self):
        for record in self:
            record.capacity = record.get_capacity()

    @api.constrains("active")
    def _check_active(self):
        for record in self:
            if not record.active and record.total_rooms_count > 0:
                raise ValidationError(
                    _("You can not archive a room type with active rooms.")
                    + " "
                    + _("Please, change the %s room(s) to other room type.")
                    % str(record.total_rooms_count)
                )

    def get_restrictions(self, date, restriction_plan_id):
        self.ensure_one()
        restriction = self.env["pms.room.type.restriction.item"].search(
            [
                ("date", "=", date),
                ("room_type_id", "=", self.id),
                ("restriction_id", "=", restriction_plan_id),
            ],
            limit=1,
        )
        return restriction

    def open_channel_bind_ids(self):
        channel_bind_ids = self.mapped("channel_bind_ids")
        action = self.env.ref("connector_pms.channel_pms_room_type_action").read()[0]
        action["views"] = [
            (self.env.ref("connector_pms.channel_pms_room_type_view_form").id, "form")
        ]
        action["target"] = "new"
        if len(channel_bind_ids) == 1:
            action["res_id"] = channel_bind_ids.ids[0]
        elif len(channel_bind_ids) > 1:
            # WARNING: more than one binding is currently not expected
            action["domain"] = [("id", "in", channel_bind_ids.ids)]
        else:
            action["context"] = {
                "default_odoo_id": self.id,
                "default_name": self.name,
                "default_ota_capacity": self.capacity,
                "default_capacity": self.capacity,
                "default_list_price": self.list_price,
                "default_total_rooms_count": self.total_rooms_count,
            }
        return action

    def disconnect_channel_bind_ids(self):
        # TODO: multichannel rooms is not implemented
        self.channel_bind_ids.with_context({"connector_no_export": True}).unlink()

    def write(self, vals):
        if "active" in vals and vals.get("active") is False:
            self.channel_bind_ids.unlink()
        return super().write(vals)
