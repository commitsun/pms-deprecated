# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create

from odoo import fields

_logger = logging.getLogger(__name__)


class ProductPricelistItemImportMapper(Component):
    _name = "channel.product.pricelist.item.import.mapper"
    _inherit = "channel.import.mapper"
    _apply_on = "channel.product.pricelist.item"

    direct = [
        ("price", "fixed_price"),
        ("date", "date_start"),
        ("date", "date_end"),
    ]

    @only_create
    @mapping
    def compute_price(self, record):
        return {"compute_price": "fixed"}

    @only_create
    @mapping
    def channel_pushed(self, record):
        return {"channel_pushed": True}

    @only_create
    @mapping
    def applied_on(self, record):
        return {"applied_on": "1_product"}

    @mapping
    def product_tmpl_id(self, record):
        return {
            "product_tmpl_id": record[
                "channel_room_type"].product_id.product_tmpl_id.id
        }

    @mapping
    def pricelist_id(self, record):
        return {"pricelist_id": record["pricelist_id"]}

    @mapping
    def backend_id(self, record):
        return {"backend_id": self.backend_record.id}

    @mapping
    def sync_date(self, record):
        return {"sync_date": fields.Datetime.now()}
