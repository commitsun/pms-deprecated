# Copyright 2017  Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PmsAvailabilityPlanRule(models.Model):
    _name = "pms.availability.plan.rule"
    _description = "Reservation rule by day"

    # Field Declarations

    availability_plan_id = fields.Many2one(
        comodel_name="pms.availability.plan",
        string="Availability Plan",
        ondelete="cascade",
        index=True,
    )
    room_type_id = fields.Many2one(
        comodel_name="pms.room.type",
        string="Room Type",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date(string="Date")

    min_stay = fields.Integer(
        string="Min. Stay",
        default=0,
    )
    min_stay_arrival = fields.Integer(
        string="Min. Stay Arrival",
        default=0,
    )
    max_stay = fields.Integer(
        string="Max. Stay",
        default=0,
    )
    max_stay_arrival = fields.Integer(
        string="Max. Stay Arrival",
        default=0,
    )
    closed = fields.Boolean(
        string="Closed",
        default=False,
    )
    closed_departure = fields.Boolean(
        string="Closed Departure",
        default=False,
    )
    closed_arrival = fields.Boolean(
        string="Closed Arrival",
        default=False,
    )
    quota = fields.Integer(
        string="Quota",
        store=True,
        readonly=False,
        compute="_compute_quota",
        help="Generic Quota assigned.",
    )
    max_avail = fields.Integer(
        string="Max. Availability",
        store=True,
        readonly=False,
        compute="_compute_max_avail",
        help="Maximum simultaneous availability on own Booking Engine.",
    )
    pms_property_id = fields.Many2one(
        comodel_name="pms.property",
        string="Property",
        ondelete="restrict",
        required=True,
    )
    allowed_property_ids = fields.Many2many(
        "pms.property",
        "allowed_availability_move_rel",
        "availability_plan_rule_id",
        "property_id",
        string="Allowed Properties",
        store=True,
        readonly=True,
        compute="_compute_allowed_property_ids",
    )
    avail_id = fields.Many2one(
        string="Avail record",
        comodel_name="pms.availability",
        compute="_compute_avail_id",
        store=True,
        readonly=False,
        ondelete="restrict",
    )
    real_avail = fields.Integer(
        related="avail_id.real_avail",
        store="True",
    )
    plan_avail = fields.Integer(
        compute="_compute_plan_avail",
        store="True",
    )

    _sql_constraints = [
        (
            "room_type_registry_unique",
            "unique(availability_plan_id, room_type_id, date, pms_property_id)",
            "Only can exists one availability rule in the same \
                         day for the same room type!",
        )
    ]

    @api.depends("room_type_id", "date", "pms_property_id")
    def _compute_avail_id(self):
        for record in self:
            if record.room_type_id and record.pms_property_id and record.date:
                avail = self.env["pms.availability"].search(
                    [
                        ("date", "=", record.date),
                        ("room_type_id", "=", record.room_type_id.id),
                        ("pms_property_id", "=", record.pms_property_id.id),
                    ]
                )
                if avail:
                    record.avail_id = avail.id
                else:
                    record.avail_id = self.env["pms.availability"].create(
                        {
                            "date": record.date,
                            "room_type_id": record.room_type_id.id,
                            "pms_property_id": record.pms_property_id.id,
                        }
                    )
            else:
                record.avail_id = False

    @api.depends("quota", "max_avail", "real_avail")
    def _compute_plan_avail(self):
        for record in self.filtered("real_avail"):
            real_avail = record.real_avail
            plan_avail = min(
                [
                    record.max_avail if record.max_avail >= 0 else real_avail,
                    record.quota if record.quota >= 0 else real_avail,
                    real_avail,
                ]
            )
            if not record.plan_avail or record.plan_avail != plan_avail:
                record.plan_avail = plan_avail

    @api.depends("room_type_id")
    def _compute_quota(self):
        for record in self:
            if not record.quota:
                record.quota = record.room_type_id.default_quota

    @api.depends("room_type_id")
    def _compute_max_avail(self):
        for record in self:
            if not record.max_avail:
                record.max_avail = record.room_type_id.default_max_avail

    @api.depends(
        "availability_plan_id.pms_property_ids", "room_type_id.pms_property_ids"
    )
    def _compute_allowed_property_ids(self):

        for rule in self:
            properties = []

            if not (
                rule.availability_plan_id.pms_property_ids
                or rule.room_type_id.pms_property_ids
            ):
                rule.allowed_property_ids = False
            else:
                if rule.availability_plan_id.pms_property_ids:
                    if rule.room_type_id.pms_property_ids:
                        for prp in rule.availability_plan_id.pms_property_ids:
                            if prp in rule.room_type_id.pms_property_ids:
                                properties.append(prp)
                        rule.allowed_property_ids = [
                            (4, prop.id) for prop in properties
                        ]
                    else:
                        rule.allowed_property_ids = (
                            rule.availability_plan_id.pms_property_ids
                        )
                else:
                    rule.allowed_property_ids = rule.room_type_id.pms_property_ids

    @api.constrains(
        "allowed_property_ids",
        "pms_property_id",
    )
    def _check_property_integrity(self):
        for rec in self:
            if rec.pms_property_id and rec.allowed_property_ids:
                if rec.pms_property_id.id not in rec.allowed_property_ids.ids:
                    raise ValidationError(_("Property not allowed"))

    # @api.constrains(
    #     "allowed_property_ids",
    #     "pms_property_ids",
    # )
    # def _check_property_integrity(self):
    #     for rule in self:
    #         for p in rule.pms_property_ids:
    #             allowed = list(
    #                 set(rule.room_type_id.pms_property_ids.ids)
    #                 &
    #                 set(rule.availability_plan_id.pms_property_ids.ids))
    #             if p.id not in allowed:
    #                 raise ValidationError(_("Property not allowed"))

    @api.constrains("min_stay", "min_stay_arrival", "max_stay", "max_stay_arrival")
    def _check_min_max_stay(self):
        for record in self:
            if record.min_stay < 0:
                raise ValidationError(_("Min. Stay can't be less than zero"))
            elif record.min_stay_arrival < 0:
                raise ValidationError(_("Min. Stay Arrival can't be less than zero"))
            elif record.max_stay < 0:
                raise ValidationError(_("Max. Stay can't be less than zero"))
            elif record.max_stay_arrival < 0:
                raise ValidationError(_("Max. Stay Arrival can't be less than zero"))
            elif (
                record.min_stay != 0
                and record.max_stay != 0
                and record.min_stay > record.max_stay
            ):
                raise ValidationError(_("Max. Stay can't be less than Min. Stay"))
            elif (
                record.min_stay_arrival != 0
                and record.max_stay_arrival != 0
                and record.min_stay_arrival > record.max_stay_arrival
            ):
                raise ValidationError(
                    _("Max. Stay Arrival can't be less than Min. Stay Arrival")
                )
