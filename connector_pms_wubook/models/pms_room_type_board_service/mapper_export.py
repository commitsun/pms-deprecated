# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.component.core import Component

# from odoo.addons.connector.components.mapper import mapping


class ChannelWubookPmsRoomTypeBoardServiceMapperExport(Component):
    _name = "channel.wubook.pms.room.type.board.service.mapper.export"
    _inherit = "channel.wubook.mapper.export"

    _apply_on = "channel.wubook.pms.room.type.board.service"

    # direct = [
    #     ("name", "name"),
    # ]
    #
    # @mapping
    # def name(self, record):
    #     return {"name": record['name']}
