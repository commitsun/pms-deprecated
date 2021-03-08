# Copyright 2017  Dario Lodeiros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models

#TODO: Cambiar nombre a PmsUbication
class PmsFloor(models.Model):
    _name = "pms.floor"
    _description = "Ubication"

    # Fields declaration
    #TODO: Estandarizar campos
    name = fields.Char(
        "Ubication Name", translate=True, required=True
    )
    pms_property_ids = fields.Many2many(
        "pms.property", string="Properties", required=False, ondelete="restrict"
    )
    #TODO: Relacion inversa con pms.room y constrain del tipo amenity_type
    sequence = fields.Integer("Sequence")
