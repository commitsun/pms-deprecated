# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create

_logger = logging.getLogger(__name__)


class PmsRoomTypeRestrictionItemImportMapper(Component):
    _name = "channel.pms.room.type.restriction.item.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.pms.room.type.restriction.item"

    direct = [
        ("min_stay", "min_stay"),
        ("min_stay_arrival", "min_stay_arrival"),
        ("max_stay", "max_stay"),
        ("max_stay_arrival", "max_stay_arrival"),
        ("closed", "closed"),
        # ('closed_departure', 'closed_departure'),
        ("closed_arrival", "closed_arrival"),
        ("date", "date"),
    ]

    @only_create
    @mapping
    def channel_pushed(self, record):
        return {"channel_pushed": True}

    @mapping
    def room_type_id(self, record):
        return {"room_type_id": record["room_type_id"]}

    @mapping
    def restriction_id(self, record):
        return {"restriction_id": record["restriction_id"]}

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def sync_date(self, record):
        return {"sync_date": fields.Datetime.now()}

    @mapping
    def closed_departure(self, record):
        return {"closed_departure": int(record["closed_departure"])}
