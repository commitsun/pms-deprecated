from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

PMS_BUSINESS_MODELS = [
    ("pms.reservation"),
    ("pms.checkin.partner"),
    ("pms.service.line"),
    ("pms.folio"),
    ("account.move"),
    ("account.payment"),
]


class AdvancedFiltersWizard(models.TransientModel):

    _name = "pms.advanced.filters.wizard"
    _description = "Wizard for advanced filters"

    pms_model_id = fields.Many2one(
        "ir.model",
        string="Recipients Model",
        ondelete="cascade",
        required=True,
        domain=[("model", "in", PMS_BUSINESS_MODELS)],
        default=lambda self: self.env.ref("pms.model_pms_reservation").id,
    )
    pms_model_name = fields.Char(
        string="Recipients Model Name",
        related="pms_model_id.model",
        readonly=True,
        related_sudo=True,
    )
    pms_domain = fields.Char(string="Domain")

    def action_filter(self):
        self.ensure_one()
        if self.pms_model_name == "pms.reservation":
            action = self.env.ref("pms.open_pms_reservation_form_tree_all").read()[0]
        if self.pms_model_name == "pms.checkin.partner":
            action = self.env.ref("pms.action_checkin_partner").read()[0]
        if self.pms_model_name == "pms.service.line":
            action = self.env.ref("pms.action_service_line").read()[0]
        if self.pms_model_name == "pms.folio":
            action = self.env.ref("pms.open_pms_folio1_form_tree_all").read()[0]
        if self.pms_model_name == "account.move":
            action = self.env.ref("account.action_move_out_invoice_type").read()[0]
        if self.pms_model_name == "account.payment":
            action = self.env.ref("account.action_account_payments").read()[0]
        domain = self.pms_domain
        if domain is not False:
            domain = safe_eval(self.pms_domain)
            action["domain"] = domain
            return action
        else:
            raise UserError(_("You must add filters to perform the search"))
