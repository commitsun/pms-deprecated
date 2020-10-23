# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ChannelWubookBackend(models.Model):
    _name = "channel.wubook.backend"
    _inherit = "connector.backend"
    _inherits = {"channel.backend": "parent_id"}
    _description = "Channel Wubook PMS Backend"

    parent_id = fields.Many2one(
        comodel_name="channel.backend",
        string="Parent Channel Backend",
        required=True,
        ondelete="cascade",
    )

    _sql_constraints = [
        (
            "backend_parent_uniq",
            "unique(parent_id)",
            "Only one backend child is allowed for each generic backend.",
        ),
    ]

    # connection data
    username = fields.Char("Username", required=True)
    password = fields.Char("Password", required=True)

    url = fields.Char(
        string="Url", default="https://wired.wubook.net/xrws/", required=True
    )
    property_code = fields.Char(string="Property code", required=True)
    pkey = fields.Char(string="PKey", required=True)

    # room type
    def import_room_types(self):
        self = self.with_user(self.user_id)
        for rec in self:
            rec.env["channel.wubook.pms.room.type"].with_delay().import_data(
                backend_record=rec
            )

    def export_room_types(self):
        self = self.with_user(self.user_id)
        for rec in self:
            rec.env["channel.wubook.pms.room.type"].with_delay().export_data(
                backend_record=rec
            )

    # room type class
    def import_room_type_classes(self):
        self = self.with_user(self.user_id)
        for rec in self:
            rec.env["channel.wubook.pms.room.type.class"].with_delay().import_data(
                backend_record=rec
            )

    def export_room_types_classes(self):
        self = self.with_user(self.user_id)
        for rec in self:
            rec.env["channel.wubook.pms.room.type.class"].with_delay().export_data(
                backend_record=rec
            )

    # pricelist
    pricelist_date_from = fields.Date("Pricelist Date From")
    pricelist_date_to = fields.Date("Pricelist Date To")
    pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        relation="wubook_backend_pricelist_rel",
        column1="backend_id",
        column2="pricelist_id",
        domain=[("pricelist_type", "=", "daily")],
    )
    # TODO: add logic to control this and filter the rooms by the current property
    room_type_ids = fields.Many2many(
        comodel_name="pms.room.type",
        relation="wubook_backend_room_type_rel",
        column1="backend_id",
        column2="room_type_id",
    )

    def import_pricelists(self):
        self = self.with_user(self.user_id)
        for rec in self:
            if rec.pricelist_date_to < rec.pricelist_date_from:
                raise UserError(_("Date to must be greater than date from"))
            rec.env["channel.wubook.product.pricelist"].with_delay().import_data(
                rec,
                rec.pricelist_date_from,
                rec.pricelist_date_to,
                rec.pricelist_ids,
                rec.room_type_ids,
            )

    # folio
    folio_date_arrival_from = fields.Date(string="Arrival Date From")
    folio_date_arrival_to = fields.Date(string="Arrival Date To")
    folio_mark = fields.Boolean(string="Mark")

    def import_folios(self):
        self = self.with_user(self.user_id)
        for rec in self:
            if rec.folio_date_arrival_to < rec.folio_date_arrival_from:
                raise UserError(_("Date to must be greater than date from"))
            # rec.env["channel.wubook.pms.folio"].import_data(
            rec.env["channel.wubook.pms.folio"].with_context(
                test_queue_job_no_delay=True
            ).with_delay().import_data(
                rec,
                rec.folio_date_arrival_from,
                rec.folio_date_arrival_to,
                rec.folio_mark,
            )
