# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class BindingPmsRoomTypeListener(Component):
    _name = "binding.pms.room.type.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["pms.room.type"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = (
            "name",
            "list_price",
            "total_rooms_count",
            "board_service_room_type_ids",
        )
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            for binding in record.channel_bind_ids:
                binding.modify_room()


class ChannelBindingRoomTypeListener(Component):
    _name = "channel.binding.room.type.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.pms.room.type"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if not record.external_id:
            record.create_room()
        else:
            record.modify_room()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_unlink(self, record, fields=None):
        record.delete_room()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        # only fields from channel.pms.room.type should be listener
        fields_to_check = (
            "ota_capacity",
            "channel_short_code",
            "min_price",
            "max_price",
            "default_availability",
        )
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            record.modify_room()
