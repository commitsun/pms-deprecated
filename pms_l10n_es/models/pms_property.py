from odoo import models, fields

class PmsProperty(models.Model):
    _inherit = "pms.property"

    police_number = fields.Char('Police number', size=10
                                )
