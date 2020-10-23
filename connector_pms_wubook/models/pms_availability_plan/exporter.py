# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.component.core import Component


class ChannelWubookPmsAvailabilityPlanDelayedBatchExporter(Component):
    _name = "channel.wubook.pms.availability.plan.delayed.batch.exporter"
    _inherit = "channel.wubook.delayed.batch.exporter"

    _apply_on = "channel.wubook.pms.availability.plan"


class ChannelWubookPmsAvailabilityPlanDirectBatchExporter(Component):
    _name = "channel.wubook.pms.availability.plan.direct.batch.exporter"
    _inherit = "channel.wubook.direct.batch.exporter"

    _apply_on = "channel.wubook.pms.availability.plan"


class ChannelWubookPmsAvailabilityPlanExporter(Component):
    _name = "channel.wubook.pms.availability.plan.exporter"
    _inherit = "channel.wubook.exporter"

    _apply_on = "channel.wubook.pms.availability.plan"
