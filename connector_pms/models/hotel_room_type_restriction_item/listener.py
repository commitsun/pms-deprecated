# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class BindingHotelRoomTypeRestrictionItemListener(Component):
    _name = "binding.hotel.room.type.restriction.item.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["hotel.room.type.restriction.item"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = (
            "min_stay",
            "min_stay_arrival",
            "max_stay",
            "max_stay_arrival",
            "closed",
            "closed_departure",
            "closed_arrival",
            "date",
        )
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            record.channel_bind_ids.write({"channel_pushed": False})

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if not any(record.channel_bind_ids):
            channel_hotel_room_type_rest_item_obj = self.env[
                "channel.hotel.room.type.restriction.item"
            ]
            for restriction_bind in record.restriction_id.channel_bind_ids:
                restriction_item_bind = channel_hotel_room_type_rest_item_obj.search(
                    [
                        ("odoo_id", "=", record.id),
                        ("backend_id", "=", restriction_bind.backend_id.id),
                    ]
                )
                if not restriction_item_bind:
                    channel_hotel_room_type_rest_item_obj.create(
                        {
                            "odoo_id": record.id,
                            "channel_pushed": False,
                            "backend_id": restriction_bind.backend_id.id,
                        }
                    )


class ChannelBindingHotelRoomTypeRestrictionItemListener(Component):
    _name = "channel.binding.hotel.room.type.restriction.item.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.hotel.room.type.restriction.item"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = (
            "min_stay",
            "min_stay_arrival",
            "max_stay",
            "max_stay_arrival",
            "closed",
            "closed_departure",
            "closed_arrival",
            "date",
        )
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            record.channel_pushed = False
