# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class PmsRoomTypeRestrictionItemExporter(Component):
    _name = "channel.pms.room.type.restriction.item.exporter"
    _inherit = "pms.channel.exporter"
    _apply_on = ["channel.pms.room.type.restriction.item"]
    _usage = "pms.room.type.restriction.item.exporter"

    @api.model
    def push_restriction(self):
        raise NotImplementedError

    @api.model
    def close_online_sales(self):
        raise NotImplementedError
