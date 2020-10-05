# Copyright 2018-2019 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime, timedelta

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if

_logger = logging.getLogger(__name__)


class BindingHotelRoomTypeAvailabilityListener(Component):
    _name = "binding.hotel.room.type.availability.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["hotel.room.type.availability"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = ("quota", "max_avail", "no_ota")
        fields_checked = [elm for elm in fields_to_check if elm in fields]

        _logger.info("==[on_record_write] :: hotel.room.type.availability==")
        _logger.info(fields)

        if any(fields_checked) and any(record.channel_bind_ids):
            if "no_ota" in fields_checked:
                self.env.context = dict(self.env.context)
                self.env.context.update({"update_no_ota": True})
            for binding in record.channel_bind_ids:
                binding.refresh_availability(
                    record.date,
                    (
                        datetime.strptime(
                            record.date, DEFAULT_SERVER_DATE_FORMAT
                        ).date()
                        + timedelta(days=1)
                    ).strftime(DEFAULT_SERVER_DATE_FORMAT),
                    binding.backend_id.id,
                    room_type_id=record.room_type_id.id,
                )

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if not any(record.channel_bind_ids):
            channel_room_type_avail_obj = self.env[
                "channel.hotel.room.type.availability"
            ]
            backends = self.env["channel.backend"].search([])
            for backend in backends:
                # REVIEW :: If you create directly channel_binding, this search
                # return empty
                avail_bind = channel_room_type_avail_obj.search(
                    [("odoo_id", "=", record.id), ("backend_id", "=", backend.id)]
                )
                if not avail_bind:
                    # REVIEW :: WARNING :: This create triggers
                    # on_record_write above
                    avail_bind = channel_room_type_avail_obj.create(
                        {
                            "odoo_id": record.id,
                            "channel_pushed": False,
                            "backend_id": backend.id,
                        }
                    )
                    _logger.info(
                        "==[on_record_create] :: hotel.room.type.availability=="
                    )
                    _logger.info(avail_bind)
                else:
                    avail_bind.refresh_availability(
                        record.date,
                        (
                            datetime.strptime(
                                record.date, DEFAULT_SERVER_DATE_FORMAT
                            ).date()
                            + timedelta(days=1)
                        ).strftime(DEFAULT_SERVER_DATE_FORMAT),
                        backend.id,
                        # room_type_id=record.room_type_id.channel_bind_ids.id,
                        room_type_id=record.room_type_id.id,
                    )


class ChannelBindingHotelRoomTypeAvailabilityListener(Component):
    _name = "channel.binding.hotel.room.type.availability.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.hotel.room.type.availability"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = ("date", "channel_avail")
        fields_checked = [elm for elm in fields_to_check if elm in fields]

        _logger.info("==[on_record_write] :: channel.hotel.room.type.availability==")
        _logger.info(fields)

        if any(fields_checked):
            # self.env['channel.backend'].cron_push_changes()
            record.with_context({"connector_no_export": True}).write(
                {"channel_pushed": False}
            )
            # record.push_availability(record.backend_id)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if any(record.channel_bind_ids):

            _logger.info(
                "==[on_record_create] :: channel.hotel.room.type.availability=="
            )
            _logger.info(fields)

            for binding in record.channel_bind_ids:
                record.refresh_availability(
                    record.date,
                    record.date,
                    binding.backend_id.id,
                    room_type_id=record.room_type_id.id,
                )
                # record.push_availability(record.backend_id)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_fix_channel_availability(self, record, fields=None):
        if any(record.channel_bind_ids):
            for binding in record.channel_bind_ids:
                record.refresh_availability(
                    record.date,
                    record.date,
                    binding.backend_id.id,
                    room_type_id=record.room_type_id.id,
                )
