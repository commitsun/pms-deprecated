# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class PmsRoomTypeRestrictionItemAdapter(Component):
    _name = "channel.pms.room.type.restriction.item.adapter"
    _inherit = "wubook.adapter"
    _apply_on = "channel.pms.room.type.restriction.item"

    def wired_rplan_get_rplan_values(
        self, date_from, date_to, channel_restriction_plan_id
    ):
        return super(
            PmsRoomTypeRestrictionItemAdapter, self
        ).wired_rplan_get_rplan_values(date_from, date_to, channel_restriction_plan_id)
