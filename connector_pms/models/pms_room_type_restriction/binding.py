# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.queue_job.job import job


class ChannelPmsRoomTypeRestriction(models.Model):
    _name = "channel.pms.room.type.restriction"
    _inherit = "channel.binding"
    _inherits = {"pms.room.type.restriction": "odoo_id"}
    _description = "Channel Pms Room Type Restriction"

    odoo_id = fields.Many2one(
        comodel_name="pms.room.type.restriction",
        string="Pms Virtual Room Restriction",
        required=True,
        ondelete="cascade",
    )

    @job(default_channel="root.channel")
    def create_plan(self):
        self.ensure_one()
        if not self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="pms.room.type.restriction.exporter")
                exporter.create_rplan(self)

    @job(default_channel="root.channel")
    def update_plan_name(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                exporter = work.component(usage="pms.room.type.restriction.exporter")
                exporter.rename_rplan(self)

    @job(default_channel="root.channel")
    def delete_plan(self):
        self.ensure_one()
        if self.external_id:
            with self.backend_id.work_on(self._name) as work:
                deleter = work.component(usage="pms.room.type.restriction.deleter")
                deleter.delete_rplan(self)

    @job(default_channel="root.channel")
    def import_restriction_plans(self, backend):
        with backend.work_on(self._name) as work:
            importer = work.component(usage="pms.room.type.restriction.importer")
            return importer.import_restriction_plans()
