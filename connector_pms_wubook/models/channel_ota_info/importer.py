# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component
from odoo.addons.connector_pms.components.core import ChannelConnectorError


class ChannelOtaInfoImporter(Component):
    _inherit = "channel.ota.info.importer"

    @api.model
    def import_otas_info(self):
        count = 0
        try:
            results = self.backend_adapter.get_channels_info()
        except ChannelConnectorError as err:
            self.create_issue(
                section="room",
                internal_message=str(err),
                channel_message=err.data["message"],
            )
        else:
            channel_ota_info_obj = self.env["channel.ota.info"]
            ota_info_mapper = self.component(
                usage="import.mapper", model_name="channel.ota.info"
            )
            for ota_id in results.keys():
                vals = {
                    "id": ota_id,
                    "name": results[ota_id]["name"],
                    "ical": results[ota_id]["ical"] == 1,
                }
                map_record = ota_info_mapper.map_record(vals)
                ota_info_bind = channel_ota_info_obj.search(
                    [
                        ("backend_id", "=", self.backend_record.id),
                        ("ota_id", "=", ota_id),
                    ],
                    limit=1,
                )
                if ota_info_bind:
                    ota_info_bind.with_context({"connector_no_export": True}).write(
                        map_record.values()
                    )
                else:
                    ota_info_bind.with_context({"connector_no_export": True}).create(
                        map_record.values(for_create=True)
                    )
                count = count + 1
        return count

    @api.model
    def push_activation(self, base_url):
        try:
            results = self.backend_adapter.push_activation(
                base_url, self.backend_record.security_token
            )
        except ChannelConnectorError as err:
            self.create_issue(
                section="channel",
                internal_message=str(err),
                channel_message=err.data["message"],
            )
            return False
        return results
