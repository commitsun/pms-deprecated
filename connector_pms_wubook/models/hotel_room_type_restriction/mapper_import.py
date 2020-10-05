# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class HotelRoomTypeRestrictionImportMapper(Component):
    _name = "channel.hotel.room.type.restriction.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.hotel.room.type.restriction"

    direct = [
        ("name", "name"),
        ("id", "external_id"),
    ]

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}
