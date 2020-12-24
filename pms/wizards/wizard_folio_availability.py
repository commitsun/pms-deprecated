from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class NumRoomsSelectionModel(models.TransientModel):
    _name = "pms.num.rooms.selection"
    _rec_name = 'name'
    name = fields.Integer()
    room_type_id = fields.Char()

    folio_wizard_id = fields.One2many(
        comodel_name="pms.folio.availability.wizard",
        inverse_name="id",
    )


class AvailabilityWizard(models.TransientModel):
    _name = "pms.folio.availability.wizard"

    num_rooms_available = fields.Integer(
        string="Available rooms",
        default=0,
    )
    room_type_description = fields.Char(
        string="Room type",
    )
    rooms_selected = fields.Integer(
        string="Selected rooms",
        default=0,
    )
    price_per_room = fields.Float(
        string="Price per room",
        default=0,
    )
    discount = fields.Float(
        string="Discount",
        default=0,
    )
    price_total = fields.Float(
        string="Total price", default=0, compute="_compute_price_total"
    )
    folio_wizard_id = fields.Many2one(
        comodel_name="pms.folio.wizard",
    )
    num_room_type_values = fields.Integer(
        compute="_compute_dynamic_selection",
        readonly=True,
        store=False,
        default=0
    )
    num_rooms_selected = fields.Many2one(
        comodel_name="pms.num.rooms.selection",
        inverse_name="folio_wizard_id",
        string="Selected rooms",
        domain="[('name', '<=', num_rooms_available), "
        "('room_type_id', '=', room_type_id)]",
    )
    value_num_rooms_selected = fields.Integer(default=0)
    room_type_id = fields.Many2one(comodel_name="pms.room.type")

    @api.depends("num_rooms_selected")
    def _compute_price_total(self):
        for record in self:
            record.price_total = record.price_per_room * record.num_rooms_selected.name
            record.value_num_rooms_selected = record.num_rooms_selected.name
            record.flush()

    @api.onchange("rooms_selected")
    def check_selected_rooms(self):
        for record in self:
            if record.rooms_selected > record.num_rooms_available:
                raise ValidationError(
                    _(
                        "You cannot indicate a room type rooms number higher "
                        "than those available."
                    )
                )

    # @api.depends("num_rooms_selected")
    def _compute_dynamic_selection(self):
        for record in self:
            record.num_room_type_values = 0
            for elem_to_insert in range(0, record.num_rooms_available + 1):
                if (
                    self.env["pms.num.rooms.selection"].search_count(
                        [
                            ("name", "=", elem_to_insert),
                            ("room_type_id", "=", record.room_type_id.id),
                        ]
                    )
                    == 0
                ):
                    self.env["pms.num.rooms.selection"].create(
                        {
                            "name": elem_to_insert,
                            "room_type_id": record.room_type_id.id,
                        }
                    )
            default = self.env["pms.num.rooms.selection"].search(
                [("name", "=", 0), ("room_type_id", "=", record.room_type_id.id)]
            )
            record.num_rooms_selected = default
