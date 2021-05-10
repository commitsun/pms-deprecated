from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class PmsReservationPatchParam(Datamodel):
    _name = "pms.reservation.patch.param"
    partner_requests = fields.String(required=True, allow_none=False)
