# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PmsReservation(models.Model):
    _inherit = "pms.reservation"

    def _set_access_for_channel_fields(self):
        for record in self:
            user = self.env["res.users"].browse(self.env.uid)
            record.able_to_modify_channel = user.has_group("base.group_system")

    # TODO: Dario v2
    # @api.depends('channel_type', 'channel_bind_ids.ota_id')
    # def _get_origin_sale(self):
    #     for record in self:
    #         if not record.channel_type:
    #             record.channel_type = 'door'
    #
    #         if record.channel_type == 'web' and any(
    #         record.channel_bind_ids) and \
    #                 record.channel_bind_ids[0].ota_id:
    #             record.origin_sale = record.channel_bind_ids[0].ota_id.name
    #         else:
    #             record.origin_sale = dict(
    #                 self.fields_get(allfields=['channel_type'])[
    #                 'channel_type']['selection']
    #             )[record.channel_type]

    channel_bind_ids = fields.One2many(
        comodel_name="channel.pms.reservation",
        inverse_name="odoo_id",
        string="Pms Channel Connector Bindings",
    )
    ota_id = fields.Many2one(
        "channel.ota.info",
        string="Channel OTA ID",
        store=True,
        compute="_compute_external_data",
    )
    ota_reservation_id = fields.Char(
        "Channel OTA Reservation Code", store=True, compute="_compute_external_data"
    )
    external_id = fields.Char(
        string="ID on Channel", store=True, compute="_compute_external_data"
    )
    # TODO: Dario v2
    # origin_sale = fields.Char('Origin', compute=_get_origin_sale,
    #                           store=True)
    is_from_ota = fields.Boolean(
        "Is From OTA", compute="_compute_external_data", store=True
    )
    able_to_modify_channel = fields.Boolean(
        compute=_set_access_for_channel_fields,
        string="Is user able to modify channel fields?",
    )
    customer_notes = fields.Text(related="folio_id.customer_notes")

    unconfirmed_channel_price = fields.Boolean(
        related="folio_id.unconfirmed_channel_price"
    )

    @api.depends(
        "channel_bind_ids.external_id",
        "channel_bind_ids.ota_id",
        "channel_bind_ids.ota_reservation_id",
    )
    def _compute_external_data(self):
        for record in self:
            is_from_ota = False
            for bind in record.channel_bind_ids:
                if bind.ota_reservation_id and bind.ota_reservation_id != "undefined":
                    is_from_ota = True
            vals = {
                "ota_reservation_id": record.channel_bind_ids[0].ota_reservation_id
                if record.channel_bind_ids
                else False,
                "ota_id": record.channel_bind_ids[0].ota_id.id
                if record.channel_bind_ids
                else False,
                "external_id": record.channel_bind_ids[0].external_id
                if record.channel_bind_ids
                else False,
                "is_from_ota": is_from_ota,
            }
            record.update(vals)

    @api.onchange("checkin", "checkout")
    def onchange_dates(self):
        if not self.is_from_ota:
            return super().onchange_dates()

    @api.model
    def create(self, vals):
        from_channel = False
        if (
            vals.get("channel_bind_ids")
            and vals.get("channel_bind_ids")[0][2]
            and vals.get("channel_bind_ids")[0][2].get("external_id") is not None
        ):
            vals.update({"preconfirm": False})
            from_channel = True
        user = self.env["res.users"].browse(self.env.uid)
        if user.has_group("pms.group_pms_call"):
            vals.update({"to_assign": True})

        reservation_id = super(PmsReservation, self).create(vals)
        backend_id = (
            self.env["channel.pms.room.type"]
            .search([("odoo_id", "=", vals["room_type_id"])])
            .backend_id
        )
        # WARNING: more than one backend_id is currently not expected
        self.env["channel.pms.room.type.availability"].sudo().refresh_availability(
            checkin=vals["real_checkin"],
            checkout=vals["real_checkout"],
            backend_id=backend_id.id,
            room_type_id=vals["room_type_id"],
            from_channel=from_channel,
        )

        return reservation_id

    def write(self, vals):
        if self._context.get("connector_no_export", True) and (
            vals.get("checkin")
            or vals.get("checkout")
            or vals.get("room_id")
            or vals.get("state")
            or "overbooking" in vals
        ):
            from_channel = False
            old_vals = []
            new_vals = []
            for record in self:
                if record.channel_bind_ids:
                    from_channel = True
                old_backend_id = (
                    self.env["channel.pms.room.type"]
                    .search([("odoo_id", "=", record.room_id.room_type_id.id)])
                    .backend_id.id
                    or None
                )
                old_vals.append(
                    {
                        "checkin": record.checkin,
                        "checkout": record.checkout,
                        "backend_id": old_backend_id,
                        "room_id": record.room_id.id,
                    }
                )
                # NOTE: A reservation can be moved into a room type not
                # connected to any channel
                new_backend_id = (
                    self.env["channel.pms.room.type"]
                    .search(
                        [("room_ids", "in", vals.get("room_id", record.room_id.id))]
                    )
                    .backend_id.id
                    or None
                )
                new_vals.append(
                    {
                        "checkin": vals.get("checkin", record.checkin),
                        "checkout": vals.get("checkout", record.checkout),
                        "backend_id": new_backend_id,
                        "room_id": vals.get("room_id", record.room_id.id),
                    }
                )

            res = super().write(vals)

            channel_room_type_avail_obj = self.env["channel.pms.room.type.availability"]
            for k_i, v_i in enumerate(old_vals):
                channel_room_type_avail_obj.sudo().refresh_availability(
                    checkin=v_i["checkin"],
                    checkout=v_i["checkout"],
                    backend_id=v_i["backend_id"],
                    room_id=v_i["room_id"],
                    from_channel=from_channel,
                )
                channel_room_type_avail_obj.sudo().refresh_availability(
                    checkin=new_vals[k_i]["checkin"],
                    checkout=new_vals[k_i]["checkout"],
                    backend_id=new_vals[k_i]["backend_id"],
                    room_id=new_vals[k_i]["room_id"],
                    from_channel=from_channel,
                )
        else:
            res = super().write(vals)
        return res

    def generate_copy_values(self, checkin=False, checkout=False):
        self.ensure_one()
        res = super().generate_copy_values(checkin=checkin, checkout=checkout)
        commands = []
        for bind_id in self.channel_bind_ids.ids:
            commands.append((4, bind_id, False))
        res.update(
            {
                "channel_bind_ids": commands,
                "customer_notes": self.customer_notes,
                "is_from_ota": self.is_from_ota,
                "to_assign": self.to_assign,
            }
        )
        return res

    def action_reservation_checkout(self):
        for record in self:
            if record.state != "cancelled":
                return super(PmsReservation, record).action_reservation_checkout()

    @api.model
    def _hcalendar_reservation_data(self, reservations):
        json_reservs, json_tooltips = super()._hcalendar_reservation_data(reservations)

        reserv_obj = self.env["pms.reservation"]
        for reserv in json_reservs:
            reservation = reserv_obj.browse(reserv["id"])
            reserv["fix_days"] = reservation.splitted or reservation.is_from_ota

        return (json_reservs, json_tooltips)

    def mark_as_readed(self):
        self.write({"to_assign": False})
