# Copyright 2017  Alexandre Díaz
# Copyright 2017  Dario Lodeiros
# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PmsRoomType(models.Model):
    """Before creating a 'room type', you need to consider the following:
    With the term 'room type' is meant a sales type of residential accommodation: for
    example, a Double Room, a Economic Room, an Apartment, a Tent, a Caravan...
    """

    _name = "pms.room.type"
    _description = "Room Type"
    _inherits = {"product.product": "product_id"}
    _order = "sequence,code_type,name"

    sequence = fields.Integer("Sequence", default=0)
    product_id = fields.Many2one(
        "product.product",
        "Product Room Type",
        required=True,
        delegate=True,
        ondelete="cascade",
    )
    room_ids = fields.One2many(
        "pms.room",
        "room_type_id",
        "Rooms",
        domain="["
        "'|', "
        "('pms_property_id', '=', False), "
        "('pms_property_id','in', pms_property_ids)"
        "]",
    )
    class_id = fields.Many2one(
        "pms.room.type.class",
        "Property Type Class",
        required=True,
        domain="["
        "'|', "
        "('pms_property_ids', '=', False), "
        "('pms_property_ids', 'in', pms_property_ids)"
        "]",
    )
    board_service_room_type_ids = fields.One2many(
        "pms.board.service.room.type",
        "pms_room_type_id",
        string="Board Services",
        domain="['|', ('pms_property_ids', '=', False), ('pms_property_ids', 'in', "
        "pms_property_ids)]",
    )
    room_amenity_ids = fields.Many2many(
        "pms.amenity",
        "pms_room_type_amenity_rel",
        "room_type_id",
        "amenity_id",
        string="Room Type Amenities",
        help="List of Amenities.",
        domain="["
        "'|', "
        "('pms_property_ids', '=', False), "
        "('pms_property_ids', 'in', pms_property_ids)"
        "]",
    )
    default_code = fields.Char(
        "Code",
        required=True,
    )
    # TODO: Session review to define shared room and "sales rooms packs"
    shared_room = fields.Boolean(
        "Shared Room", default=False, help="This room type is reservation by beds"
    )
    total_rooms_count = fields.Integer(compute="_compute_total_rooms_count", store=True)
    default_max_avail = fields.Integer(
        "Default Max. Availability",
        default=-1,
        help="Maximum simultaneous availability on own Booking Engine "
        "given no availability rules. "
        "Use `-1` for using maximum simultaneous availability.",
    )
    default_quota = fields.Integer(
        "Default Quota",
        default=-1,
        help="Quota assigned to the own Booking Engine given no availability rules. "
        "Use `-1` for managing no quota.",
    )

    def name_get(self):
        result = []
        for room_type in self:
            name = room_type.name
            if self._context.get("checkin") and self._context.get("checkout"):
                avail = self.env[
                    "pms.room.type.availability.plan"
                ].get_count_rooms_available(
                    checkin=self._context.get("checkin"),
                    checkout=self._context.get("checkout"),
                    room_type_id=room_type.id,
                    pms_property_id=self._context.get("pms_property_id") or False,
                    pricelist_id=self._context.get("pricelist_id") or False,
                )
                name += " (%s)" % avail
            result.append((room_type.id, name))
        return result

    @api.depends("room_ids", "room_ids.active")
    def _compute_total_rooms_count(self):
        for record in self:
            record.total_rooms_count = len(record.room_ids)

    @api.model
    def get_room_types_by_property(self, pms_property_id, code_type=None):
        """
        :param pms_property_id: property ID
        :param code_type: room type code (optional)
        :return: - recordset of
                    - all the pms.room.type of the pms_property_id
                      if code_type not defined
                    - one or 0 pms.room.type if code_type defined
                 - ValidationError if more than one code_type found by
                   the same pms_property_id
        """
        domain = []
        if code_type:
            domain += ["&", ("code_type", "=", code_type)]
        company_id = self.env["pms.property"].browse(pms_property_id).company_id.id
        domain += [
            "|",
            ("pms_property_ids", "in", pms_property_id),
            "|",
            "&",
            ("pms_property_ids", "=", False),
            ("company_id", "=", company_id),
            "&",
            ("pms_property_ids", "=", False),
            ("company_id", "=", False),
        ]
        records = self.search(domain)
        res, res_priority = {}, {}
        for rec in records:
            res_priority.setdefault(rec.code_type, -1)
            priority = (rec.pms_property_ids and 2) or (rec.company_id and 1 or 0)
            if priority > res_priority[rec.code_type]:
                res.setdefault(rec.code_type, rec.id)
                res[rec.code_type], res_priority[rec.code_type] = rec.id, priority
            elif priority == res_priority[rec.code_type]:
                raise ValidationError(
                    _(
                        "Integrity error: There's multiple room types "
                        "with the same code %s and properties"
                    )
                    % rec.code_type
                )
        return self.browse(list(res.values()))

    @api.constrains("pms_property_ids", "class_id")
    def _check_integrity_property_class(self):
        for record in self:
            if record.pms_property_ids and record.class_id.pms_property_ids:
                for pms_property in record.pms_property_ids:
                    if pms_property.id not in record.class_id.pms_property_ids.ids:
                        raise ValidationError(
                            _("Property isn't allowed in Room Type Class")
                        )

    @api.constrains("code_type", "pms_property_ids", "company_id")
    def _check_code_property_company_uniqueness(self):
        msg = _("Already exists another room type with the same code and properties")
        for rec in self:
            if not rec.pms_property_ids:
                if self.search(
                    [
                        ("id", "!=", rec.id),
                        ("code_type", "=", rec.code_type),
                        ("pms_property_ids", "=", False),
                        ("company_id", "=", rec.company_id.id),
                    ]
                ):
                    raise ValidationError(msg)
            else:
                for pms_property in rec.pms_property_ids:
                    other = rec.get_room_types_by_property(
                        pms_property.id, rec.code_type
                    )
                    if other and other != rec:
                        raise ValidationError(msg)

    @api.constrains("room_amenity_ids", "pms_property_ids")
    def _check_integrity_property_amenity(self):
        for record in self:
            if record.room_amenity_ids.pms_property_ids and record.pms_property_ids:
                for pms_property in record.pms_property_ids:
                    if pms_property not in record.room_amenity_ids.pms_property_ids:
                        raise ValidationError(_("Property not allowed in amenity"))

    @api.constrains("room_ids", "pms_property_ids")
    def _check_integrity_property_room(self):
        for record in self:
            if record.room_ids and record.pms_property_ids:
                for room in record.room_ids:
                    if room.pms_property_id not in record.pms_property_ids:
                        raise ValidationError(_("Property not allowed in room"))

    # TODO: Not allowed repeat boardservice on room_type with
    # same properties os without properties
    @api.constrains("board_service_room_type_ids", "pms_property_ids")
    def _check_integrity_property_board_service_room_type(self):
        for record in self:
            if record.board_service_room_type_ids and record.pms_property_ids:
                for board_service_room_type in record.board_service_room_type_ids:
                    if board_service_room_type.pms_property_ids:
                        for pms_property in record.pms_property_ids:
                            if (
                                pms_property
                                not in board_service_room_type.pms_property_ids
                            ):
                                raise ValidationError(
                                    _("Property not allowed in board service room type")
                                )

    # ORM Overrides
    # TODO: Review Check product fields default values to room
    @api.model
    def create(self, vals):
        """ Add room types as not purchase services. """
        vals.update(
            {
                "purchase_ok": False,
                "sales_ok": False,
                "type": "service",
            }
        )
        return super().create(vals)

    # TODO: Check if this is necesary
    def unlink(self):
        for record in self:
            record.product_id.unlink()
        return super().unlink()

    # Business methods

    def get_capacity(self):
        self.ensure_one()
        capacities = self.room_ids.mapped("capacity")
        return min(capacities) if any(capacities) else 0
