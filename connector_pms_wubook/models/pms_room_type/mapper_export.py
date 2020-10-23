# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ChannelWubookPmsRoomTypeMapperExport(Component):
    _name = "channel.wubook.pms.room.type.mapper.export"
    _inherit = "channel.wubook.mapper.export"

    _apply_on = "channel.wubook.pms.room.type"

    direct = [
        ("default_code", "shortname"),
        ("name", "name"),
        ("occupancy", "occupancy"),
        # ("default_availability", "availability"),
        ("default_board", "board"),
        ("list_price", "price"),
        ("min_price", "min_price"),
        ("max_price", "max_price"),
    ]

    @mapping
    def woodoo(self, record):
        return {"woodoo": 0}

    @mapping
    def occupancy(self, record):
        return {"availability": len(record["room_ids"])}
