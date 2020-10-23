# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PmsRoomTypeAvailabilityRule(models.Model):
    _inherit = "pms.availability.plan.rule"

    no_ota = fields.Boolean(
        string="No OTA",
        default=False,
        help="Set zero availability to the connected OTAs "
        "even when the availability is positive,"
        "except to the Online Reception (booking engine)",
    )
