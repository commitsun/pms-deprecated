# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector_pms.components.core import ChannelConnectorError


class ProductPricelistImportMapper(Component):
    _name = "channel.product.pricelist.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.product.pricelist"

    direct = [
        ("id", "external_id"),
        ("name", "name"),
    ]

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def pricelist_type(self, record):
        if record["daily"] == 1:
            return {"pricelist_type": "daily"}
        else:
            # TODO: manage not daily plans in Hootel
            raise ChannelConnectorError(
                _("Can't map a pricing plan from wubook"), {"message": ""}
            )
