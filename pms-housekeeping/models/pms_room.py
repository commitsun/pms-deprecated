# Copyright 2021 Jose Luis Algara (Alda Hotels <https://www.aldahotels.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import fields, models


class PmsRoom(models.Model):
    _inherit = "pms.room"

    clean_status = fields.Selection(
        string="Clean Status",
        selection=[
            ("occupied", "Occupied"),
            ("exit", "Exit"),
            ("picked_up", "Picked up"),
            ("staff", "Staff"),
            ("clean", "Clean"),
            ("inspected", "Inspected"),
            ("dont_disturb", "Don't disturb"),
        ],
        default="clean",
    )

    housekeeping_ids = fields.One2many(
        string="Housekeeping tasks",
        comodel_name="pms.housekeeping",
        inverse_name="room_id",
        compute="_compute_housekeeping_tasks",
        store=True,
        readonly=True,
    )

    clean_status_now = fields.Char(
        "Clean Status 2",
        compute="_compute_clean_status",
    )

    def _compute_housekeeping_tasks(self):
        for room in self:
            tasks = self.env["pms.housekeeping"].search(
                [
                    ("room_id", "=", room.id),
                    ("task_date", "=", datetime.now().date()),
                ]
            )
            # Debug Stop -------------------
            # import wdb
            # wdb.set_trace()
            # Debug Stop -------------------
            self.housekeeping_ids = tasks
        return tasks

    # @api.depends('clean_status_now')
    def _compute_clean_status(self):
        for room in self:
            room.clean_status_now = room.get_clean_status()
        return

    # Business methods

    def get_clean_status(self, date_clean=datetime.now().date(), margin_days=5):
        status = "NONE"
        reservations = self.env["pms.reservation.line"].search(
            [
                ("room_id", "=", self.id),
                ("date", "<=", date_clean + timedelta(days=margin_days)),
                ("date", ">=", date_clean - timedelta(days=margin_days)),
            ]
        )
        today_res = reservations.filtered(
            lambda reservation: reservation.date == date_clean
        )
        yesterday_res = reservations.filtered(
            lambda reservation: reservation.date == date_clean - (timedelta(days=1))
        )
        lasts_res = reservations.filtered(
            lambda reservation: reservation.date < date_clean
        )

        if today_res.reservation_id.reservation_type == "out":
            status = "dont_disturb"
            return status
        if len(today_res) == 0:
            if len(yesterday_res) != 0:
                status = "exit"
            elif len(lasts_res) != 0:
                status = "clean"
            else:
                # TODO hace cauntos dias se limpio o repaso.??
                status = "picked_up"
        else:
            if yesterday_res.reservation_id != today_res.reservation_id:
                status = "exit"
            else:
                if today_res.reservation_id.reservation_type == "staff":
                    status = "staff"
                elif today_res.reservation_id.dont_disturb:
                    status = "dont_disturb"
                else:
                    status = "occupied"
                    # TODO hace cauntos dias que la ocupa.??
        return status
