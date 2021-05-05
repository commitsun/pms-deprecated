from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class PmsRoomTypeShortInfo(Datamodel):
    _name = "pms.room.type.short.info"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
