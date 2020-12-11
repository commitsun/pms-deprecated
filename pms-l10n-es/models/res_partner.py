from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    document_type = fields.Selection([
        ('D', 'DNI'),
        ('P', 'Pasaporte'),
        ('C', 'Permiso de Conducir'),
        ('I', 'Carta o Doc. de Identidad'),
        ('N', 'Permiso Residencia Español'),
        ('X', 'Permiso Residencia Europeo')],
        help=_('Select a valid document type'),
        string='Doc. type',
    )
    document_number = fields.Char(
        string='Document number',
    )
    document_expedition_date = fields.Date(
        string='Documento expedition date'
    )


