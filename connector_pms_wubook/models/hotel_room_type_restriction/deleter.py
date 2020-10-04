# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector_pms.components.core import ChannelConnectorError


class HotelRoomTypeRestrictionDeleter(Component):
    _inherit = "channel.hotel.room.type.restriction.deleter"

    @api.model
    def delete_rplan(self, binding):
        try:
            return self.backend_adapter.delete_rplan(binding.external_id)
        except ChannelConnectorError as err:
            self.create_issue(
                section="restriction",
                internal_message=str(err),
                channel_message=err.data["message"],
            )
            raise ValidationError(_(err.data["message"]) + ". " + _(str(err)))
