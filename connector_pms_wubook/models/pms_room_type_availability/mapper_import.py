# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create

_logger = logging.getLogger(__name__)


class PmsRoomTypeAvailabilityImportMapper(Component):
    _name = "channel.pms.room.type.availability.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.pms.room.type.availability"

    direct = [
        ("no_ota", "no_ota"),
        ("booked", "booked"),
        ("avail", "channel_avail"),
        ("avail", "quota"),
        ("date", "date"),
    ]

    @only_create
    @mapping
    def channel_pushed(self, record):
        return {"channel_pushed": True}

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def room_type_id(self, record):
        return {"room_type_id": record["room_type_id"]}

    @mapping
    def sync_date(self, record):
        return {"sync_date": fields.Datetime.now()}
