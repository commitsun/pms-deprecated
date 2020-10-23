# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

from odoo.addons.component.core import Component
from odoo.addons.queue_job.job import job
from odoo import exceptions


class ChannelWubookPmsRoomTypeBinding(models.Model):
    _name = 'channel.wubook.pms.room.type'
    _inherits = {'channel.pms.room.type': 'parent_id'}

    parent_id = fields.Many2one(comodel_name='channel.pms.room.type',
                              string='Room Type Binding',
                              required=True,
                              ondelete='cascade')

    # @job(default_channel='root.channel')
    # @api.model
    # def import_data(self, backend_record=None):
    #     """ Prepare the batch import of room types from Channel """
    #     return self.import_batch(backend=backend_record)

    # @api.multi
    # def resync(self):
    #     for record in self:
    #         with record.backend_id.work_on(record._name) as work:
    #             binder = work.component(usage='binder')
    #             relation = binder.unwrap_binding(self)
    #
    #         func = record.import_record
    #         if record.env.context.get('connector_delay'):
    #             func = record.import_record.delay
    #
    #         func(record.backend_id, relation)
    #
    #     return True
