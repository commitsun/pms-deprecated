# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class PmsFolio(models.Model):
    _inherit = "pms.folio"

    wseed = fields.Char("Wubook Session Seed", readonly=True)
