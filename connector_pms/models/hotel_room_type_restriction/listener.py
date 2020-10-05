# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class BindingHotelRoomTypeListener(Component):
    _name = "binding.hotel.room.type.restriction.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["hotel.room.type.restriction"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        if "name" in fields:
            for binding in record.channel_bind_ids:
                binding.update_plan_name()


class ChannelBindingHotelRoomTypeRestrictionListener(Component):
    _name = "channel.binding.hotel.room.type.restriction.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.hotel.room.type.restriction"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.create_plan()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_unlink(self, record, fields=None):
        record.delete_plan()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        if "name" in fields:
            record.update_plan_name()
