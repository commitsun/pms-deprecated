# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_auto_done_setting = fields.Boolean("Lock Confirmed Sales", implied_group='sale.group_auto_done_setting')
    module_sale_margin = fields.Boolean("Margins")
    quotation_validity_days = fields.Integer(related='company_id.quotation_validity_days', string="Default Quotation Validity (Days)", readonly=False)
    use_quotation_validity_days = fields.Boolean("Default Quotation Validity", config_parameter='sale.use_quotation_validity_days')
    group_warning_sale = fields.Boolean("Sale Order Warnings", implied_group='sale.group_warning_sale')
    portal_confirmation_sign = fields.Boolean(related='company_id.portal_confirmation_sign', string='Online Signature', readonly=False)
    portal_confirmation_pay = fields.Boolean(related='company_id.portal_confirmation_pay', string='Online Payment', readonly=False)
    group_sale_delivery_address = fields.Boolean("Customer Addresses", implied_group='sale.group_delivery_invoice_address')
    group_proforma_sales = fields.Boolean(string="Pro-Forma Invoice", implied_group='sale.group_proforma_sales',
        help="Allows you to send pro-forma invoice.")
    default_pms_invoice_policy = fields.Selection([
        ('order', 'Invoice what is ordered'),
        ('checkout', 'Invoice what is delivered')
        ], 'Invoicing Policy Reservation',
        default='checkout',
        default_model='pms.room.type')
    deposit_default_pms_product_id = fields.Many2one(
        'product.product',
        'Deposit Product',
        domain="[('type', '=', 'service')]",
        config_parameter='pms.default_pms_deposit_product_id',
        help='Default product used for payment advances on reservations')

    auth_signup_uninvited = fields.Selection([
        ('b2b', 'On invitation'),
        ('b2c', 'Free sign up'),
    ], string='Customer Account', default='b2b', config_parameter='auth_signup.invitation_scope')

    module_product_email_template = fields.Boolean("Specific Email")
    module_sale_coupon = fields.Boolean("Coupons & Promotions")

    automatic_invoice = fields.Boolean("Automatic Invoice",
                                       help="The invoice is generated automatically and available in the customer portal "
                                            "when the transaction is confirmed by the payment acquirer.\n"
                                            "The invoice is marked as paid and the payment is registered in the payment journal "
                                            "defined in the configuration of the payment acquirer.\n"
                                            "This mode is advised if you issue the final invoice at the order and not after the delivery.",
                                       config_parameter='sale.automatic_invoice')
    template_id = fields.Many2one('mail.template', 'Email Template',
                                  domain="[('model', '=', 'account.move')]",
                                  config_parameter='sale.default_email_template',
                                  default=lambda self: self.env.ref('account.email_template_edi_invoice', False))
    confirmation_template_id = fields.Many2one('mail.template', string='Confirmation Email',
                                               domain="[('model', '=', 'sale.order')]",
                                               config_parameter='sale.default_confirmation_template',
                                               help="Email sent to the customer once the order is paid.")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        if self.default_invoice_policy != 'order':
            self.env['ir.config_parameter'].set_param('sale.automatic_invoice', False)

    @api.onchange('use_quotation_validity_days')
    def _onchange_use_quotation_validity_days(self):
        if self.quotation_validity_days <= 0:
            self.quotation_validity_days = self.env['res.company'].default_get(['quotation_validity_days'])['quotation_validity_days']

    @api.onchange('quotation_validity_days')
    def _onchange_quotation_validity_days(self):
        if self.quotation_validity_days <= 0:
            self.quotation_validity_days = self.env['res.company'].default_get(['quotation_validity_days'])['quotation_validity_days']
            return {
                'warning': {'title': "Warning", 'message': "Quotation Validity is required and must be greater than 0."},
            }
