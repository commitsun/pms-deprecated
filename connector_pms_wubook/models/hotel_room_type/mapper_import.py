# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class HotelRoomTypeImportMapper(Component):
    _name = "channel.hotel.room.type.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.hotel.room.type"

    direct = [
        ("id", "external_id"),
        ("shortname", "channel_short_code"),
        ("occupancy", "ota_capacity"),
        ("price", "list_price"),
        ("name", "name"),
    ]

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def class_id(self, record):
        return {"class_id": record["class_id"]}
