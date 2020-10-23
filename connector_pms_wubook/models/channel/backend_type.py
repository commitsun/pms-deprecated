# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ChannelBackend(models.Model):
    _inherit = "channel.backend.type"

    @api.model
    def _get_channel_backend_type_model_names(self):
        res = super(ChannelBackend, self)._get_channel_backend_type_model_names()
        res.append("channel.wubook.backend.type")
        return res


class ChannelWubookBackendType(models.Model):
    _name = "channel.wubook.backend.type"
    _inherits = {"channel.backend.type": "parent_id"}
    _description = "Channel Wubook PMS Backend Type"

    _main_model = "channel.wubook.backend"

    parent_id = fields.Many2one(
        comodel_name="channel.backend.type",
        string="Parent Channel Backend Type",
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

    # room type class map
    room_type_class_ids = fields.One2many(
        string="Room type classes",
        comodel_name="channel.wubook.backend.type.room.type.class",
        inverse_name="backend_type_id",
    )

    # board service map
    board_service_ids = fields.One2many(
        string="Board services",
        comodel_name="channel.wubook.backend.type.board.service",
        inverse_name="backend_type_id",
    )
