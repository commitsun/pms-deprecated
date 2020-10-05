# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PmsRoomTypeRestrictionItem(models.Model):
    _inherit = "pms.room.type.restriction.item"

    channel_bind_ids = fields.One2many(
        comodel_name="channel.pms.room.type.restriction.item",
        inverse_name="odoo_id",
        string="Pms Channel Connector Bindings",
    )
