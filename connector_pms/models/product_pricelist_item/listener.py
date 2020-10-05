# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class BindingProductPricelistItemListener(Component):
    _name = "binding.product.pricelist.item.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["product.pricelist.item"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = ("date_start", "date_end", "fixed_price", "product_tmpl_id")
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            record.channel_bind_ids.write({"channel_pushed": False})

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        if not any(record.channel_bind_ids):
            channel_product_pricelist_item_obj = self.env[
                "channel.product.pricelist.item"
            ]
            for pricelist_bind in record.pricelist_id.channel_bind_ids:
                pricelist_item_bind = channel_product_pricelist_item_obj.search(
                    [
                        ("odoo_id", "=", record.id),
                        ("backend_id", "=", pricelist_bind.backend_id.id),
                    ]
                )
                if not pricelist_item_bind:
                    channel_product_pricelist_item_obj.create(
                        {
                            "odoo_id": record.id,
                            "channel_pushed": False,
                            "backend_id": pricelist_bind.backend_id.id,
                        }
                    )


class ChannelBindingProductPricelistItemListener(Component):
    _name = "channel.binding.product.pricelist.item.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["channel.product.pricelist.item"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        fields_to_check = ("date_start", "date_end", "fixed_price", "product_tmpl_id")
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            record.channel_pushed = False
