# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.queue_job.job import job

from odoo import api, fields, models


class ChannelProductPricelistItem(models.Model):
    _name = "channel.product.pricelist.item"
    _inherit = "channel.binding"
    _inherits = {"product.pricelist.item": "odoo_id"}
    _description = "Channel Product Pricelist Item"

    odoo_id = fields.Many2one(
        comodel_name="product.pricelist.item",
        string="Hotel Product Pricelist Item",
        required=True,
        ondelete="cascade",
    )
    channel_pushed = fields.Boolean(
        "Channel Pushed", readonly=True, default=False, old_name="wpushed"
    )

    @job(default_channel="root.channel")
    @api.model
    def import_pricelist_values(self, backend, dfrom, dto, external_id):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="product.pricelist.item.importer")
            if not backend.pricelist_id:
                return importer.import_all_pricelist_values(dfrom, dto)
            return importer.import_pricelist_values(external_id, dfrom, dto)

    @job(default_channel="root.channel")
    @api.model
    def push_pricelist(self, backend):
        with backend.work_on(self._name) as work:
            exporter = work.component(usage="product.pricelist.item.exporter")
            return exporter.push_pricelist()
