# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ChannelBinding(models.AbstractModel):
    _name = "channel.binding"
    _inherit = "external.binding"
    _description = "Pms Channel Connector Binding (abstract)"

    backend_id = fields.Many2one(
        comodel_name="channel.backend",
        string="Pms Channel Connector Backend",
        required=True,
        ondelete="restrict",
    )

    external_id = fields.Char(string="ID on Channel")

    _sql_constraints = [
        (
            "channel_uniq",
            "unique(backend_id, external_id)",
            "A binding already exists with the same Channel ID.",
        ),
    ]
