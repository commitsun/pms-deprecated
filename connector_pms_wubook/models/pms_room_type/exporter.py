# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.component.core import Component


class ChannelWubookPmsRoomTypeDelayedBatchExporter(Component):
    _name = "channel.wubook.pms.room.type.delayed.batch.exporter"
    _inherit = "channel.wubook.delayed.batch.exporter"

    _apply_on = "channel.wubook.pms.room.type"


class ChannelWubookPmsRoomTypeDirectBatchExporter(Component):
    _name = "channel.wubook.pms.room.type.direct.batch.exporter"
    _inherit = "channel.wubook.direct.batch.exporter"

    _apply_on = "channel.wubook.pms.room.type"


class ChannelWubookPmsRoomTypeExporter(Component):
    _name = "channel.wubook.pms.room.type.exporter"
    _inherit = "channel.wubook.exporter"

    _apply_on = "channel.wubook.pms.room.type"
