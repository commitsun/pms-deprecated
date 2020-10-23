# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PmsRoomType(models.Model):
    _inherit = "pms.room.type"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.pms.room.type",
        inverse_name="odoo_id",
        string="Channel PMS Bindings",
    )
