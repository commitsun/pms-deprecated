# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PmsRoomTypeRestriction(models.Model):
    _inherit = "pms.room.type.restriction"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.pms.room.type.restriction",
        inverse_name="odoo_id",
        string="Pms Channel Connector Bindings",
    )

    @api.depends("name")
    def name_get(self):
        room_type_restriction_obj = self.env["pms.room.type.restriction"]
        org_names = super(PmsRoomTypeRestriction, self).name_get()
        names = []
        for name in org_names:
            restriction_id = room_type_restriction_obj.browse(name[0])
            new_name = name[1]
            if any(restriction_id.channel_bind_ids):
                for restriction_bind in restriction_id.channel_bind_ids:
                    if restriction_bind.external_id:
                        new_name += " (%s Backend)" % restriction_bind.backend_id.name
                names.append((name[0], new_name))
            else:
                names.append((name[0], name[1]))
        return names

    def open_channel_bind_ids(self):
        channel_bind_ids = self.mapped("channel_bind_ids")
        action = self.env.ref(
            "connector_pms.channel_pms_room_type_restriction_action"
        ).read()[0]
        action["views"] = [
            (
                self.env.ref(
                    "connector_pms.channel_pms_room_type_restriction_view_form"
                ).id,
                "form",
            )
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
            }
        return action

    def disconnect_channel_bind_ids(self):
        # TODO: multichannel rooms is not implemented
        self.channel_bind_ids.with_context({"connector_no_export": True}).unlink()

    def write(self, vals):
        if "active" in vals and vals.get("active") is False:
            self.channel_bind_ids.unlink()
        return super().write(vals)
