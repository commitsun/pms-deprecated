# Copyright 2020 Jose Luis Algara (Alda Hotels <https://www.aldahotels.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HouseKeeping(models.Model):
    _name = "pms.housekeeping"
    _description = "HouseKeeping"
    # HouseKeeping 'log'

    # Fields declaration
    cleandate = fields.Datetime(
        string="Clean dateate", default=lambda self: fields.Datetime.now()
    )
    room = fields.Many2one("pms.room", string="Room")
    employee = fields.Many2one("hr.employee", string="Employee")
    tasks = fields.Many2many("pms.housekeeping.task", string="Tasks")
    notes = fields.Text("Internal Notes")
