# Copyright 2017  Dario Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PmsUbication(models.Model):
    _name = "pms.ubication"
    _description = "Ubication"

    name = fields.Char(
        string="Ubication Name",
        help="Ubication Name",
        required=True,
        translate=True,
    )
    pms_property_ids = fields.Many2many(
        string="Properties",
        help="Properties with access to the element;"
        " if not set, all properties can access",
        comodel_name="pms.property",
        relation="pms_ubication_pms_property_rel",
        column1="ubication_type_id",
        column2="pms_property_id",
        ondelete="restrict",
    )
    # TODO: rooms in view? (amenity)
    pms_room_ids = fields.One2many(
        string="Rooms",
        help="Rooms found in this location",
        comodel_name="pms.room",
        inverse_name="ubication_id",
    )
    sequence = fields.Integer(
        string="Sequence",
        help="Field used to change the position of the ubications in tree view."
        "Changing the position changes the sequence",
    )

    @api.constrains(
        "pms_property_ids",
        "pms_room_ids",
    )
    def _check_property_integrity(self):
        for rec in self:
            if rec.pms_property_ids:
                if rec.pms_room_ids.pms_property_id not in rec.pms_property_ids:
                    raise ValidationError(_("Property not allowed"))
