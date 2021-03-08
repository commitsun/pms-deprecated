# Copyright 2017  Alexandre Díaz
# Copyright 2017  Dario Lodeiros
# Copyright 2018  Pablo Quesada
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PmsRoom(models.Model):
    """The rooms for lodging can be for sleeping, usually called rooms,
    and also for speeches (conference rooms), parking,
    relax with cafe con leche, spa...
    """

    _name = "pms.room"
    _description = "Property Room"
    _order = "sequence, room_type_id, name"

    name = fields.Char(
        string="Room Name",
        required=True,
    )
    pms_property_id = fields.Many2one(
        comodel_name="pms.property",
        required=True,
        ondelete="restrict",
        default=lambda self: self.env.user.active_property_ids[0],
    )
    room_type_id = fields.Many2one(
        "pms.room.type",
        "Property Room Type",
        required=True,
        ondelete="restrict",
        domain=[
            "|",
            ("pms_property_ids", "=", False),
            (pms_property_id, "in", "pms_property_ids"),
        ],
    )
    # TODO: Dario, design shared rooms
    shared_room_id = fields.Many2one(
        string="Shared Room",
        comodel_name="pms.shared.room",
        default=False,
    )
    ubication_id = fields.Many2one(
        comodel_name="pms.ubication",
        string="Ubication",
        help="At which ubication the room is located.",
        domain=[
            "|",
            ("pms_property_ids", "=", False),
            (pms_property_id, "in", "pms_property_ids"),
        ],
    )
    capacity = fields.Integer(
        string="Capacity"
    )
    #TODO: Eliminar campo to_be_cleaned
    to_be_cleaned = fields.Boolean(
        string="To be Cleaned",
        default=False
    )
    extra_beds_allowed = fields.Integer(
        string="Extra beds allowed",
        default="0",
        required=True
    )
    description_sale = fields.Text(
        string="Sale Description",
        translate=True,
        help="A description of the Product that you want to communicate to "
        " your customers. This description will be copied to every Sales "
        " Order, Delivery Order and Customer Invoice/Credit Note",
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
    sequence = fields.Integer(
        string="Sequence",
        default=0
    )

    allowed_property_ids = fields.Many2many(
        comodel_name="pms.property",
        relation="room_property_rel",
        column1="room_id",
        column2="property_id",
        string="Allowed properties",
        store=True,
        readonly=True,
        compute="_compute_allowed_property_ids",
    )

    # Defaults and Gets
    def name_get(self):
        result = []
        for room in self:
            name = room.name
            if room.room_type_id:
                name += " [%s]" % room.room_type_id.code_type
            result.append((room.id, name))
        return result

    @api.depends(
        "room_type_id",
        "room_type_id.pms_property_ids",
        "ubication_id",
        "ubication_id.pms_property_ids",
    )
    #TODO: Dario, revisar flujo de allowed properties
    def _compute_allowed_property_ids(self):
        for record in self:
            if not (
                record.room_type_id.pms_property_ids or record.ubication_id.pms_property_ids
            ):
                record.allowed_property_ids = self.env["pms.property"].search([])
            elif not record.room_type_id.pms_property_ids:
                record.allowed_property_ids = record.ubication_id.pms_property_ids
            elif not record.ubication_id.pms_property_ids:
                record.allowed_property_ids = record.room_type_id.pms_property_ids
            else:
                record.allowed_property_ids = record.room_type_id.pms_property_ids & record.ubication_id.pms_property_ids

    # Constraints and onchanges
    @api.constrains("capacity")
    def _check_capacity(self):
        for record in self:
            if record.capacity < 1:
                raise ValidationError(
                    _(
                        "The capacity of the \
                        room must be greater than 0."
                    )
                )

    @api.constrains(
        "allowed_property_ids",
        "pms_property_id",
    )
    def _check_property_integrity(self):
        for rec in self:
            if rec.pms_property_id:
                if rec.pms_property_id.id not in rec.allowed_property_ids.ids:
                    raise ValidationError(
                        _("Property not allowed in room type or in floor")
                    )

    # Business methods
    def get_capacity(self, extra_bed=0):
        if not self.shared_room_id:
            return self.capacity + extra_bed
        return self.capacity
