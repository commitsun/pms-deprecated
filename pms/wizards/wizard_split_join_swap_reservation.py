import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ReservationSplitJoinSwapWizard(models.TransientModel):
    _name = "pms.reservation.split.join.swap.wizard"
    main_options = fields.Selection(
        [
            ("swap", "Swap rooms"),
            ("split", "Split reservation"),
            ("join", "Join reservation"),
        ],
        string="Operation",
        default="swap",
    )
    reservation_id = fields.Many2one(
        string="Reservation",
        comodel_name="pms.reservation",
        default=lambda self: self.env["pms.reservation"]
        .browse(self._context.get("active_id"))
        .id
        if self._context.get("active_id")
        else False,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
    )
    pms_property_id = fields.Many2one(
        string="Pms Property",
        default=lambda self: self.env.user.get_active_property_ids()[0],
        comodel_name="pms.property",
    )
    checkin = fields.Date(
        string="Check In",
    )
    checkout = fields.Date(
        string="Check Out",
    )
    reservations = fields.Many2many(
        string="Reservations",
        comodel_name="pms.reservation",
        compute="_compute_reservations",
        store=True,
        readonly=False,
    )
    room_source = fields.Many2one(
        string="Room Source",
        comodel_name="pms.room",
        domain="[('id', 'in', allowed_room_sources)]",
    )
    capacity_room_source = fields.Integer(
        string="Capacity of selected room",
        store=True,
        readonly=False,
        compute="_compute_capacity_room_source",
    )
    allowed_room_sources = fields.Many2many(
        string="Allowed rooms source",
        comodel_name="pms.room",
        compute="_compute_allowed_rooms_source",
        store=True,
        readonly=False,
    )
    room_target = fields.Many2one(
        string="Room Target",
        comodel_name="pms.room",
        domain="[('id', '!=', room_source), ('capacity', '>=', capacity_room_source )]",
    )
    reservation_lines_to_change = fields.One2many(
        comodel_name="pms.wizard.reservation.lines.split",
        inverse_name="reservation_wizard_id",
        compute="_compute_reservation_lines",
        store=True,
        readonly=False,
    )

    @api.depends("checkin", "checkout", "room_source", "room_target")
    def _compute_reservations(self):
        for record in self:
            if record.checkin and record.checkout:
                reservation_ids = list()
                for date_iterator in [
                    record.checkin + datetime.timedelta(days=x)
                    for x in range(0, (record.checkout - record.checkin).days)
                ]:
                    lines = self.env['pms.reservation.line'].search(
                        [
                            ('date', '=', date_iterator),
                        ]
                    )
                    reservation_ids.extend(
                        lines.mapped('reservation_id').ids
                    )
                reservation_ids = list(set(reservation_ids))
                reservations = self.env['pms.reservation'].search(
                    [
                        ('id', 'in', reservation_ids)
                    ]
                )
                record.reservations = reservations

                if record.room_source and record.room_target:
                    record.reservations = record.reservations.filtered(
                        lambda x: record.room_source
                        in x.reservation_line_ids.mapped("room_id")
                        or record.room_target
                        in x.reservation_line_ids.mapped("room_id")
                    )
            else:
                record.reservations = False

    @api.depends("reservation_id")
    def _compute_reservation_lines(self):
        for record in self:
            if record.reservation_id:
                cmds = [(5, 0, 0)]
                for line in record.reservation_id.reservation_line_ids:
                    cmds.append(
                        (
                            0,
                            0,
                            {
                                "reservation_wizard_id": record.id,
                                "room_id": line.room_id,
                                "date": line.date,
                            },
                        )
                    )
                    record.reservation_lines_to_change = cmds
            else:
                record.reservation_lines_to_change = False

    @api.depends("checkin", "checkout")
    def _compute_allowed_rooms_source(self):
        for record in self:
            record.allowed_room_sources = (
                record.reservations.reservation_line_ids.mapped("room_id")
            )

    @api.depends("room_source")
    def _compute_capacity_room_source(self):
        for record in self:
            record.capacity_room_source = False
            if record.room_source:
                record.capacity_room_source = record.room_source.capacity

    @api.model
    def reservation_split(self, reservation, date, room):
        if not reservation:
            raise UserError(_("Invalid reservation"))
        if not reservation or not reservation.reservation_line_ids.filtered(
            lambda x: x.date == date
        ):
            raise UserError(_("Invalid date for reservation line "))

        if not self.browse(room.id):
            raise UserError(_("The room does not exist"))
        rooms_available = self.env["pms.availability.plan"].rooms_available(
            checkin=date,
            checkout=(
                datetime.datetime(year=date.year, month=date.month, day=date.day)
                + datetime.timedelta(days=1)
            ).date(),
            current_lines=reservation.reservation_line_ids.ids,
            pricelist_id=reservation.pricelist_id.id,
            pms_property_id=reservation.pms_property_id.id,
        )
        if room not in rooms_available:
            raise UserError(_("The room is not available"))

        reservation.reservation_line_ids.filtered(
            lambda x: x.date == date
        ).room_id = room.id

    @api.model
    def reservation_unify(self, reservation, room):
        rooms_available = self.env["pms.availability.plan"].rooms_available(
            checkin=reservation.checkin,
            checkout=reservation.checkout,
            current_lines=reservation.reservation_line_ids.ids,
            pricelist_id=reservation.pricelist_id.id,
            pms_property_id=reservation.pms_property_id.id,
        )
        if room in rooms_available:
            for line in (
                self.env["pms.reservation"]
                .search([("id", "=", reservation.id)])
                .reservation_line_ids
            ):
                line.room_id = room
        else:
            raise UserError(_("Room {} not available.".format(room.name)))

    @api.model
    def reservations_swap(self, checkin, checkout, source, target):
        for date_iterator in [
            checkin + datetime.timedelta(days=x)
            for x in range(0, (checkout - checkin).days)
        ]:
            line_room_source = self.env['pms.reservation.line'].search(
                [
                    ("date", "=", date_iterator),
                    ("room_id", "=", source)
                ]
            )
            line_room_target = self.env['pms.reservation.line'].search(
                [
                    ("date", "=", date_iterator),
                    ("room_id", "=", target)
                ]
            )
            if line_room_source and line_room_target:

                # this causes an unique error constraint
                line_room_target.occupies_availability = False
                line_room_source.occupies_availability = False

                line_room_target.room_id = source
                line_room_source.room_id = target

                line_room_target._compute_occupies_availability()
                line_room_source._compute_occupies_availability()

            else:
                line_room_source.room_id = target

    def action_split(self):
        for record in self:
            for line in record.reservation_lines_to_change:
                self.reservation_split(
                    record.reservation_id,
                    line.date,
                    line.room_id,
                )

    def action_unify(self):
        for record in self:
            self.reservation_unify(record.reservation_id, record.room_target)

    def action_swap(self):
        self.reservations_swap(
            self.checkin, self.checkout, self.room_source.id, self.room_target.id
        )


class ReservationLinesToSplit(models.TransientModel):
    _name = "pms.wizard.reservation.lines.split"

    reservation_wizard_id = fields.Many2one(
        comodel_name="pms.reservation.split.join.swap.wizard",
    )
    date = fields.Date(
        string="Date",
    )
    room_id = fields.Many2one(
        string="Room",
        comodel_name="pms.room",
    )


# class ReservationsToSwap(models.Model):
#     _inherit = "pms.reservation"
#     _order = "rooms, checkin asc, checkout asc"

