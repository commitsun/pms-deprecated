# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

from odoo import fields


class ChannelOtaInfoImportMapper(Component):
    _name = "channel.ota.info.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.ota.info"

    direct = [
        ("id", "ota_id"),
        ("name", "name"),
        ("ical", "ical"),
    ]

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def sync_date(self, record):
        return {"sync_date": fields.Datetime.now()}
