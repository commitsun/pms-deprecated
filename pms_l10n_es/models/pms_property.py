<<<<<<< HEAD
from odoo import models, fields
=======
from odoo import fields, models

>>>>>>> 131523d... [WIP]pms_l10n_es: traveller report with limit in sequence

class PmsProperty(models.Model):
    _inherit = "pms.property"

<<<<<<< HEAD
    police_number = fields.Char('Police number', size=10
                                )
=======
    police_type = fields.Selection(
        [
            ("guardia_civil", "Guardia Civil"),
            ("policia_nacional", "Policía Nacional"),
            ("ertxaintxa", "Ertxaintxa"),
            ("mossos", "Mossos_d'esquadra"),
        ],
        string="Police Type",
        default="guardia_civil",
    )
    police_number = fields.Char("Police Number", size=10)
    police_user = fields.Char("Police User")
    police_pass = fields.Char("Police Password")
>>>>>>> 131523d... [WIP]pms_l10n_es: traveller report with limit in sequence
