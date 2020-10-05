# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if
from odoo.addons.connector_pms_wubook.components.backend_adapter import (
    WUBOOK_STATUS_GOOD,
)


class BindingPmsReservationListener(Component):
    _name = "binding.pms.reservation.listener"
    _inherit = "base.connector.listener"
    _apply_on = ["pms.reservation"]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):

        fields_to_check = ("state",)
        fields_checked = [elm for elm in fields_to_check if elm in fields]
        if any(fields_checked):
            if any(record.channel_bind_ids):
                # Only can cancel reservations created directly in wubook
                for binding in record.channel_bind_ids:
                    if (
                        binding.external_id
                        and not binding.ota_id
                        and int(binding.channel_status) in WUBOOK_STATUS_GOOD
                    ):
                        if record.state in ("cancelled"):
                            binding.sudo().cancel_reservation()
                        # self.env['channel.pms.reservation']._event(
                        # 'on_record_cancel').notify(binding)
