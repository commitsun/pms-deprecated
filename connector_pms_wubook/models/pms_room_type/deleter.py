# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector_pms.components.core import ChannelConnectorError


class PmsRoomTypeDeleter(Component):
    _inherit = "channel.pms.room.type.deleter"

    @api.model
    def delete_room(self, binding):
        try:
            return self.backend_adapter.delete_room(binding.external_id)
        except ChannelConnectorError as err:
            self.create_issue(
                section="room",
                internal_message=str(err),
                channel_message=err.data["message"],
            )
            raise ValidationError(_(err.data["message"]) + ". " + _(str(err)))
