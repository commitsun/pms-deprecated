# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector_pms_wubook.components.backend_adapter import (
    WUBOOK_STATUS_ACCEPTED,
    WUBOOK_STATUS_CANCELLED,
    WUBOOK_STATUS_CANCELLED_PENALTY,
    WUBOOK_STATUS_CONFIRMED,
    WUBOOK_STATUS_REFUSED,
    WUBOOK_STATUS_WAITING,
)

from odoo import fields, models


class ChannelHotelReservation(models.Model):
    _inherit = "channel.hotel.reservation"

    channel_status = fields.Selection(
        selection_add=[
            (str(WUBOOK_STATUS_CONFIRMED), "Confirmed"),
            (str(WUBOOK_STATUS_WAITING), "Waiting"),
            (str(WUBOOK_STATUS_REFUSED), "Refused"),
            (str(WUBOOK_STATUS_ACCEPTED), "Accepted"),
            (str(WUBOOK_STATUS_CANCELLED), "Cancelled"),
            (str(WUBOOK_STATUS_CANCELLED_PENALTY), "Cancelled with penalty"),
        ]
    )
    modified_reservations = fields.Char("Code Modifications")

    # TODO: Review where to check the total room amount
    # @api.model
    # def create(self, vals):
    #     record = super(ChannelHotelReservation, self).create(vals)
    #     if record.channel_total_amount !=
    #     record.odoo_id.price_room_services_set:
    #         record.odoo_id.unconfirmed_channel_price = True
    #         self.env['hotel.channel.connector.issue'].create({
    #             'backend_id': record.backend_id.id,
    #             'section': 'reservation',
    #             'internal_message': "Disagreement in reservation price.
    #             Odoo marked %.2f whereas the channel sent %.2f." % (
    #                 record.odoo_id.price_room_services_set,
    #                 record.channel_total_amount),
    #             'channel_message': 'Please, review the board services
    #             included in the reservation.',
    #             'channel_object_id': record.external_id
    #         })
    #
    #     return record
