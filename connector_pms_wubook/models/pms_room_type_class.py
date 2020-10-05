# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, models
from openerp.exceptions import ValidationError


class PmsRoomTypeClass(models.Model):
    _inherit = "pms.room.type.class"

    _locked_codes = ("1", "2", "3", "4", "5", "6", "7", "8")

    def write(self, vals):
        for record in self:
            if record.code_class in self._locked_codes:
                raise ValidationError(_("Can't modify channel room type class"))
        return super(PmsRoomTypeClass, self).write(vals)

    def unlink(self):
        for record in self:
            if record.code_class in self._locked_codes:
                raise ValidationError(_("Can't delete channel room type class"))
        return super(PmsRoomTypeClass, self).unlink()
