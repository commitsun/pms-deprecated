from odoo import models, api
class PmsCheckinPartner(models.Model):
    _inherit = "pms.checkin.partner"

    @api.model
    def _checkin_mandatory_fields(self, depends=False):
        super(PmsCheckinPartner,self)
        return ["name","lastname2","bithdate","document_number","document_expedition_date","gender"]
