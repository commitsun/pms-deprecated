# Copyright 2017  Alexandre Díaz
# Copyright 2017  Dario Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pms_property_ids = fields.Many2many(
        string="Properties",
        help="Properties with access to the element;"
        " if not set, all properties can access",
        comodel_name="pms.property",
        relation="product_template_pms_property_rel",
        column1="product_tmpl_id",
        column2="pms_property_id",
        required=False,
        ondelete="restrict",
    )
    per_day = fields.Boolean(
        string="Unit increment per day", help="Indicates it is a unit increment per day"
    )
    per_person = fields.Boolean(
        string="Unit increment per person",
        help="Indicates it is a unit increment per person",
    )
    consumed_on = fields.Selection(
        string="Consumed",
        help="Indicates when the product is consumed",
        selection=[("before", "Before night"), ("after", "After night")],
        default="before",
    )
    daily_limit = fields.Integer(
        string="Daily limit", help="Indicates how much products can consumed in one day"
    )
    is_extra_bed = fields.Boolean(
        string="Is extra bed",
        help="Indicates if that product is a extra bed",
        default=False,
    )
    is_show_in_calendar = fields.Boolean(
        string="Show in Calendar",
        help="Specifies if the product is shown in the calendar information.",
        default=False,
    )

    @api.constrains("pms_property_ids", "company_id")
    def _check_property_company_integrity(self):
        for rec in self:
            if rec.company_id and rec.pms_property_ids:
                property_companies = rec.pms_property_ids.mapped("company_id")
                if len(property_companies) > 1 or rec.company_id != property_companies:
                    raise ValidationError(
                        _(
                            "The company of the properties must match "
                            "the company on the room type"
                        )
                    )
