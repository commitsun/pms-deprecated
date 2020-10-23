# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import random

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import changed_by, mapping, only_create


class ChannelWubookPmsRoomTypeMapperImport(Component):
    _name = "channel.wubook.pms.room.type.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.pms.room.type"

    direct = [
        ("name", "name"),
        ("occupancy", "occupancy"),
        ("availability", "default_availability"),
        ("board", "default_board"),
        ("price", "list_price"),
        ("min_price", "min_price"),
        ("max_price", "max_price"),
    ]

    children = [
        (
            "boards",
            "board_service_room_type_ids",
            "channel.wubook.pms.room.type.board.service",
        ),
    ]

    # @changed_by('board')
    # @mapping #('board', 'default_board')
    # def board(self, record):
    #     return {"default_board": record['board']}

    @only_create
    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @only_create
    @mapping
    def default_code(self, record):
        return {
            "default_code": record["shortname"],
        }

    @mapping
    def class_id(self, record):
        binder = self.binder_for("channel.wubook.pms.room.type.class")
        room_type_class = binder.to_internal(record["rtype"], unwrap=True)
        return {
            "class_id": room_type_class.id,
        }

    @mapping
    def room_ids(self, record):
        room_ids = []
        binding = self.options.get("binding")
        if binding:
            room_ids = binding.room_ids.filtered(
                lambda x: x.pms_property_id == self.backend_record.pms_property_id
            ).ids

        diff_rooms = record["availability"] - len(room_ids)
        if diff_rooms < 0:
            raise NotImplementedError(
                _("Found more rooms on PMS Room Type '%s' than on the backend")
                % (binding.default_code,)
            )
        elif diff_rooms > 0:
            return {
                "room_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "TEMP-%s" % format(random.randint(0, 0xFFFF), "x"),
                            "pms_property_id": self.backend_record.pms_property_id.id,
                            "capacity": record["occupancy"],
                        },
                    )
                    for x in range(diff_rooms)
                ]
            }

    @mapping
    def property_ids(self, record):
        binding = self.options.get("binding")
        has_pms_properties = binding and bool(binding.pms_property_ids)
        if self.options.for_create or has_pms_properties:
            return {
                "pms_property_ids": [(4, self.backend_record.pms_property_id.id, 0)]
            }


class ChannelWubookPmsRoomTypeBoardServiceChildMapperImport(Component):
    _name = "channel.wubook.pms.room.type.board.service.child.mapper.import"
    _inherit = "channel.wubook.child.mapper.import"
    _apply_on = "channel.wubook.pms.room.type.board.service"
