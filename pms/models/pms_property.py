# Copyright 2019  Pablo Quesada
# Copyright 2019  Dario Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_partner import _tz_get


class PmsProperty(models.Model):
    _name = "pms.property"
    _description = "Property"
    _inherits = {"res.partner": "partner_id"}
    _check_company_auto = True

    # Fields declaration
    # TODO: Estandarización de campos
    partner_id = fields.Many2one(
        "res.partner", "Property", required=True, ondelete="cascade"
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        help="The company that owns or operates this property.",
    )
    user_ids = fields.Many2many(
        "res.users",
        "pms_property_users_rel",
        "pms_property_id",
        "user_id",
        string="Accepted Users",
    )
    room_ids = fields.One2many("pms.room", "pms_property_id", "Rooms")
    # TODO: establecer tarifa publica por defecto
    default_pricelist_id = fields.Many2one(
        "product.pricelist",
        string="Product Pricelist",
        required=True,
        help="The default pricelist used in this property.",
    )
    default_arrival_hour = fields.Char(
        string="Arrival Hour",
        help="HH:mm Format",
        default="14:00"
    )
    default_departure_hour = fields.Char(
        string="Departure Hour",
        help="HH:mm Format",
        default="12:00"
    )

    # TODO: borrar los 2 siguientes campos (tb vista)
    default_cancel_policy_days = fields.Integer(
        string="Cancellation Days",
    )
    default_cancel_policy_percent = fields.Float(
        string="Percent to pay",
    )

    # TODO: eliminar ir.sequence del pms
    # ( y la vista) y adaptar los metoddos de los create para coger la secuencia.

    folio_sequence_id = fields.Many2one(
        string="Folio Sequence",
        comodel_name="ir.sequence",
        check_company=True,
        copy=False,
        required=True,
    )
    reservation_sequence_id = fields.Many2one(
        string="Folio Sequence",
        comodel_name="ir.sequence",
        check_company=True,
        copy=False,
        required=True,
    )
    checkin_sequence_id = fields.Many2one(
        string="Checkin Sequence",
        comodel_name="ir.sequence",
        check_company=True,
        copy=False,
        required=True,
    )
    tz = fields.Selection(
        _tz_get,
        string="Timezone",
        required=True,
        default=lambda self: self.env.user.tz or "UTC",
        help="This field is used to determine de timezone of the property.",
    )

    # Constraints and onchanges
    @api.constrains("default_arrival_hour")
    def _check_arrival_hour(self):
        for record in self:
            try:
                time.strptime(record.default_arrival_hour, "%H:%M")
                return True
            except ValueError:
                raise ValidationError(
                    _(
                        "Format Arrival Hour (HH:MM) Error: %s",
                        record.default_arrival_hour,
                    )
                )

    @api.constrains("default_departure_hour")
    def _check_departure_hour(self):
        for record in self:
            try:
                time.strptime(record.default_departure_hour, "%H:%M")
                return True
            except ValueError:
                raise ValidationError(
                    _(
                        "Format Departure Hour (HH:MM) Error: %s",
                        record.default_departure_hour,
                    )
                )

    def date_property_timezone(self, dt):
        '''
        TODO: Eric explicar método
        Property hour: 12:00 (-1), UTC hour: 13:00 (0), User hour: 14:00 (+1)
        dt: 12:00 - char field with property hour
        '''
        self.ensure_one()
        tz_property = self.tz #(-1)
        dt = pytz.timezone(tz_property).localize(dt) #dt = 12 (-1)
        dt = dt.replace(tzinfo=None) #dt = 12
        dt = pytz.timezone(self.env.user.tz).localize(dt) #dt = 12 (+1)
        dt = dt.astimezone(pytz.utc) #dt = 13 (+0)
        dt = dt.replace(tzinfo=None)  #dt = 13
        return dt

    def _get_payment_methods(self):
        self.ensure_one()
        payment_methods = self.env["account.journal"].search(
            [
                "&",
                ("type", "in", ["cash", "bank"]),
                "|",
                ("pms_property_ids", "in", self.id),
                "|",
                "&",
                ("pms_property_ids", "=", False),
                ("company_id", "=", self.company_id.id),
                "&",
                ("pms_property_ids", "=", False),
                ("company_id", "=", False),
            ]
        )
        return payment_methods
