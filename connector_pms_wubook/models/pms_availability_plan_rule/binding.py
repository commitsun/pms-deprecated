# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ChannelWubookPmsAvailabilityPlanRuleBinding(models.Model):
    _name = "channel.wubook.pms.availability.plan.rule"
    _inherit = "channel.wubook.binding"
    _inherits = {"pms.availability.plan.rule": "odoo_id"}

    odoo_id = fields.Many2one(
        comodel_name="pms.availability.plan.rule",
        string="Odoo ID",
        required=True,
        ondelete="cascade",
    )
