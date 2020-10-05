# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class PmsRoomTypeAdapter(Component):
    _name = "channel.pms.room.type.adapter"
    _inherit = "wubook.adapter"
    _apply_on = "channel.pms.room.type"

    def create_room(
        self,
        shortcode,
        name,
        capacity,
        price,
        availability,
        defboard,
        names,
        descriptions,
        boards,
        min_price,
        max_price,
        rtype,
    ):
        return super(PmsRoomTypeAdapter, self).create_room(
            shortcode,
            name,
            capacity,
            price,
            availability,
            defboard,
            names,
            descriptions,
            boards,
            min_price,
            max_price,
            rtype,
        )

    def fetch_rooms(self):
        return super(PmsRoomTypeAdapter, self).fetch_rooms()

    def modify_room(
        self,
        channel_room_id,
        name,
        capacity,
        price,
        availability,
        scode,
        defboard,
        names,
        descriptions,
        boards,
        min_price,
        max_price,
        rtype,
    ):
        return super(PmsRoomTypeAdapter, self).modify_room(
            channel_room_id,
            name,
            capacity,
            price,
            availability,
            scode,
            defboard,
            names,
            descriptions,
            boards,
            min_price,
            max_price,
            rtype,
        )

    def delete_room(self, channel_room_id):
        return super(PmsRoomTypeAdapter, self).delete_room(channel_room_id)
