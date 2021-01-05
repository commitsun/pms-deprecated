# Copyright 2021 Jose Luis Algara (Alda Hotels <https://www.aldahotels.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HouseKeepingRooms(models.Model):
    _name = "pms.room_rack"
    _description = "HouseKeeping Rooms"
    # HouseKeeping 'Rooms' status (Rack)

    # Fields declaration
    rack_date = fields.Date(
        string="Rack Date",
        default=fields.Date.context_today,
    )
    room = fields.Many2one("pms.room", string="Room")
    employee = fields.Many2one("hr.employee", string="Employee")

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
    )
