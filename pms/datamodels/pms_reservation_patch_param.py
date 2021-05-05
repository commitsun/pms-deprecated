# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class PmsReservationSearchParam(Datamodel):
    _name = "pms.reservation.patch.param"
    partner_requests = fields.String(required=True, allow_none=False)
