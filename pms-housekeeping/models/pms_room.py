# Copyright 2021 Jose Luis Algara (Alda Hotels <https://www.aldahotels.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime, timedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PmsRoom(models.Model):
    _inherit = "pms.room"

    housekeeping_ids = fields.One2many(
        string="Housekeeping tasks",
        comodel_name="pms.housekeeping",
        inverse_name="room_id",
        domain=[("task_date", "=", datetime.now().date())],
    )

    clean_status = fields.Selection(
        string="Clean type",
        selection=[
            ("occupied", "Occupied"),
            ("exit", "Exit"),
            ("picked_up", "Picked up"),
            ("staff", "Staff"),
            ("clean", "Clean"),
            ("inspected", "Inspected"),
            ("dont_disturb", "Don't disturb"),
        ],
        compute="_compute_clean_status",
        # store=True,
    )

    employee_id = fields.Many2one("hr.employee", string="Assigned employee")
    employee_picture = fields.Binary(
        string="Employee picture", related="employee_id.image_1920"
    )

    # @api.depends('clean_status_now')
    def _compute_clean_status(self):
        for room in self:
            room.clean_status = room.get_clean_status()
        return

    # Business methods
    def get_clean_status(self, date_clean=False, margin_days=5):
        status = "NONE"
        if not date_clean:
            date_clean = fields.Date.today()
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
                # TODO hace cuantos dias se limpio o repaso.??
                status = "picked_up"
            return status
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
                    # TODO hace cuantos dias que la ocupa.??
        return status

    def add_today_tasks(self):
        # Debug Stop -------------------
        # import wdb
        # wdb.set_trace()
        # Debug Stop -------------------
        for room in self:
            tasks = self.env["pms.housekeeping.task"].search(
                [("clean_type", "=", room.clean_status)]
            )
            for task in tasks:
                new_task = self.env["pms.housekeeping"]
                new_task.create(
                    {
                        "room_id": room.id,
                        "employee_id": room.employee_id.id,
                        "task_id": task.id,
                        "state": "draft",
                    }
                )
        return

    def add_all_today_tasks(self):
        rooms = self.env["pms.room"].search([])
        _logger.warning("Init Add All today Task")
        for room in rooms:
            room.add_today_tasks()
        return
