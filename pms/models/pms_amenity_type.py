# Copyright 2017  Alexandre Díaz
# Copyright 2017  Dario Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PmsRoomAmenityType(models.Model):
    _name = "pms.amenity.type"
    _description = "Amenities Type"

    # Fields declaration
    name = fields.Char(
        string="Amenity Type Name",
        required=True,
        translate=True,
    )
    pms_property_ids = fields.Many2many(
        string="Properties",
        comodel_name="pms.property",
        required=False,
        ondelete="restrict",
    )
    room_amenity_ids = fields.One2many(
        comodel_name="pms.amenity",
        inverse_name="room_amenity_type_id",
        string="Amenities in this category"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )

    # TODO: Constrain coherence pms_property_ids with amenities pms_property_ids
