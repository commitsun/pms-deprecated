# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.queue_job.job import job


class ChannelPmsRoomTypeRestrictionItem(models.Model):
    _name = "channel.pms.room.type.restriction.item"
    _inherit = "channel.binding"
    _inherits = {"pms.room.type.restriction.item": "odoo_id"}
    _description = "Channel PMS Room Type Restriction Item"

    odoo_id = fields.Many2one(
        comodel_name="pms.room.type.restriction.item",
        string="Pms Virtual Room Restriction",
        required=True,
        ondelete="cascade",
    )
    channel_pushed = fields.Boolean(
        "Channel Pushed", readonly=True, default=False, old_name="wpushed"
    )

    @job(default_channel="root.channel")
    @api.model
    def import_restriction_values(self, backend, dfrom, dto, external_id):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="pms.room.type.restriction.item.importer")
            return importer.import_restriction_values(
                dfrom, dto, channel_restr_id=external_id
            )

    @job(default_channel="root.channel")
    @api.model
    def push_restriction(self, backend):
        with backend.work_on(self._name) as work:
            exporter = work.component(usage="pms.room.type.restriction.item.exporter")
            return exporter.push_restriction()

    @job(default_channel="root.channel")
    @api.model
    def close_online_sales(self, backend):
        with backend.work_on(self._name) as work:
            exporter = work.component(usage="pms.room.type.restriction.item.exporter")
            return exporter.close_online_sales()
