# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class PmsRoomTypeRestrictionAdapter(Component):
    _name = "channel.pms.room.type.restriction.adapter"
    _inherit = "wubook.adapter"
    _apply_on = "channel.pms.room.type.restriction"

    def rplan_rplans(self):
        return super(PmsRoomTypeRestrictionAdapter, self).rplan_rplans()

    def create_rplan(self, name):
        return super(PmsRoomTypeRestrictionAdapter, self).create_rplan(name)

    def delete_rplan(self, external_id):
        return super(PmsRoomTypeRestrictionAdapter, self).delete_rplan(external_id)

    def rename_rplan(self, external_id, new_name):
        return super(PmsRoomTypeRestrictionAdapter, self).rename_rplan(
            external_id, new_name
        )
