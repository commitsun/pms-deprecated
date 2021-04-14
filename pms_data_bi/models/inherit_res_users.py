# Copyright 2019 Pablo Quesada
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # Fields declaration
    data_bi_days = fields.Integer(
        string="Days to download data", required=False, default=60
    )
