# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if

_logger = logging.getLogger(__name__)


class BindingProductPricelistListener(Component):
    _name = "binding.product.pricelist.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["product.pricelist"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        if "name" in fields:
            for binding in record.channel_bind_ids:
                binding.update_plan_name()
        if "item_ids" in fields and record.pricelist_type == "virtual":
            for binding in record.channel_bind_ids:
                binding.modify_vplan()


class ChannelBindingProductPricelistListener(Component):
    _name = "channel.binding.product.pricelist.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.product.pricelist"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if record.pricelist_type == "daily":
            record.create_plan()
        elif record.pricelist_type == "virtual":
            record.create_vplan()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_unlink(self, record, fields=None):
        record.delete_plan()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        if "name" in fields:
            record.update_plan_name()
