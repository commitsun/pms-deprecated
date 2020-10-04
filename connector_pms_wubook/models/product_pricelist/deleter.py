# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector_pms.components.core import ChannelConnectorError


class ProductPricelistDeleter(Component):
    _inherit = "channel.product.pricelist.deleter"

    @api.model
    def delete_plan(self, binding):
        try:
            return self.backend_adapter.delete_plan(binding.external_id)
        except ChannelConnectorError as err:
            self.create_issue(
                section="pricelist",
                internal_message=str(err),
                channel_message=err.data["message"],
            )
            raise ValidationError(_(err.data["message"]) + ". " + _(str(err)))
