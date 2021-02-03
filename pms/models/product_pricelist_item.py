# Copyright 2017  Alexandre Díaz, Pablo Quesada, Darío Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    pms_property_ids = fields.Many2many(
        "pms.property", string="Properties", required=False, ondelete="restrict"
    )
    date_start_overnight = fields.Date(
        string="Start Date Overnight",
        help="Start date to apply daily pricelist items",
    )
    date_end_overnight = fields.Date(
        string="End Date Overnight",
        help="End date to apply daily pricelist items",
    )
