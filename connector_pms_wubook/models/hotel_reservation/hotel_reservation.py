# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector_pms_wubook.components.backend_adapter import (
    WUBOOK_STATUS_BAD,
)

from odoo import _, models
from odoo.exceptions import ValidationError


class HotelReservation(models.Model):
    _inherit = "hotel.reservation"

    def action_cancel(self):
        for record in self:
            # Can't cancel in Odoo
            if record.is_from_ota and self._context.get("ota_limits", True):
                raise ValidationError(_("Can't cancel reservations from OTA's"))
        user = self.env["res.users"].browse(self.env.uid)
        if user.has_group("hotel.group_hotel_call"):
            self.write({"to_assign": True})

        return super(HotelReservation, self).action_cancel()

    def confirm(self):
        for record in self:
            if record.is_from_ota:
                for binding in record.channel_bind_ids:
                    if int(
                        binding.channel_status
                    ) in WUBOOK_STATUS_BAD and self._context.get("ota_limits",
                                                                 True):
                        raise ValidationError(
                            _("Can't confirm OTA's cancelled reservations")
                        )
        return super(HotelReservation, self).confirm()
