# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class ChannelWubookPmsReservationLineMapperImport(Component):
    _name = "channel.wubook.pms.reservation.line.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.pms.reservation.line"

    direct = [
        ("price", "price"),
        ("day", "date"),
    ]

    # @mapping
    # def lines(self, record):
    #     return {
    #         'price': record['price'],
    #         'date': record['day'],
    #     }
