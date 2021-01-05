# Copyright 2021 Jose Luis Algara (Alda Hotels <https://www.aldahotels.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
    )
