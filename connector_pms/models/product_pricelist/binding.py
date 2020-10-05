# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

from odoo.addons.queue_job.job import job

_logger = logging.getLogger(__name__)


class ChannelProductPricelist(models.Model):
    _name = "channel.product.pricelist"
    _inherit = "channel.binding"
    _inherits = {"product.pricelist": "odoo_id"}
    _description = "Channel Product Pricelist"

    odoo_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Pricelist",
        required=True,
        ondelete="cascade",
    )

    @job(default_channel="root.channel")
    def create_plan(self):
        self.ensure_one()
        if not self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="product.pricelist.exporter")
                exporter.create_plan(self)

    @job(default_channel="root.channel")
    def create_vplan(self):
        self.ensure_one()
        if not self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="product.pricelist.exporter")
                exporter.create_vplan(self)

    @job(default_channel="root.channel")
    def modify_vplan(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="product.pricelist.exporter")
                exporter.modify_vplan(self)

    @job(default_channel="root.channel")
    def update_plan_name(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="product.pricelist.exporter")
                exporter.update_plan_name(self)

    @job(default_channel="root.channel")
    def delete_plan(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                deleter = work.component(usage="product.pricelist.deleter")
                deleter.delete_plan(self)

    @job(default_channel="root.channel")
    def import_price_plans(self, backend):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="product.pricelist.importer")
            return importer.import_pricing_plans()
