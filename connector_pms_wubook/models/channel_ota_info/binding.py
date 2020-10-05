# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ChannelOtaInfo(models.Model):
    _inherit = "channel.ota.info"

    ical = fields.Boolean("ical", default=False)
