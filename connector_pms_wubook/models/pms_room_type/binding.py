# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ChannelWubookPmsRoomTypeBinding(models.Model):
    _name = "channel.wubook.pms.room.type"
    _inherit = "channel.wubook.binding"
    _inherits = {"pms.room.type": "odoo_id"}

    @api.model
    def _default_max_avail(self):
        return (
            self.env["pms.room.type"]
            .browse(self._context.get("default_odoo_id"))
            .total_rooms_count
            or -1
        )

    @api.model
    def _default_availability(self):
        return max(min(self.default_quota, self.default_max_avail), 0)

    # binding fields
    odoo_id = fields.Many2one(
        comodel_name="pms.room.type",
        string="Odoo ID",
        required=True,
        ondelete="cascade",
    )

    # model fields
    # TODO: are these fields really necessary??
    occupancy = fields.Integer(
        string="Occupancy",
        default=1,
        help="The occupancy/capacity/beds of the rooms (children included)",
    )
    default_quota = fields.Integer(
        string="Default Quota",
        help="Quota assigned to the channel given no availability rules. "
        "Use `-1` for managing no quota.",
    )
    default_max_avail = fields.Integer(
        string="Max. Availability",
        default=_default_max_avail,
        help="Maximum simultaneous availability given no availability rules. "
        "Use `-1` for using maximum simultaneous availability.",
    )
    default_availability = fields.Integer(
        string="Availability",
        default=_default_availability,
        readonly=True,
        help="Default availability for OTAs. "
        "The availability is calculated based on the quota, "
        "the maximum simultaneous availability and "
        "the total room count for the given room type.",
    )
    default_board = fields.Char(
        string="Default board",
        default="nb",
        readonly=True,
        help="Default board service",
    )
    min_price = fields.Float(
        "Min. Price",
        default=5.0,
        digits="Product Price",
        help="Setup the min price to prevent incidents while editing your prices.",
    )
    max_price = fields.Float(
        "Max. Price",
        default=200.0,
        digits="Product Price",
        help="Setup the max price to prevent incidents while editing your prices.",
    )

    # TODO: Is this check really needed???
    # @api.constrains('min_price', 'max_price')
    # def _check_min_max_price(self):
    #     for rec in self:
    #         if rec.min_price < 5 or rec.max_price < 5:
    #             raise ValidationError(
    #                 _("The channel manager limits the minimum value "
    #                   "of min price and max price to 5."))

    @api.model
    def export_data(self, backend_record=None):
        """ Prepare the batch export of Room Types to Channel """
        room_types = self.odoo_id.get_unique_by_property_code(
            backend_record.pms_property_id.id
        )
        return self.export_batch(
            backend_record=backend_record, domain=[("id", "in", room_types.ids)]
        )

    # def write(self, values):
    #     # workaround to surpass an Odoo bug in a delegation inheritance
    #     # of pms.room.type that does not let to write 'name' field
    #     # if 'items_ids' is written as well on the same write call.
    #     # With other fields like 'sequence' it does not crash but it does not
    #     # save the value entered. For other fields it works but it's unstable.
    #     boards = values.pop("board_service_room_type_ids", None)
    #     if boards:
    #         super(ChannelWubookPmsRoomTypeBinding, self).write({"board_service_room_type_ids": boards})
    #     if values:
    #         return super(ChannelWubookPmsRoomTypeBinding, self).write(values)

    # "men": 5,
    # "subroom": 0,
    # "occupancy": 5,
    # "board": "ai",
    # "availability": 5,
    # "shortname": "H217",
    # "children": 0,
    # "boards": "",
    # "anchorate": 0,
    # "dec_avail": 0,
    # "woodoo": 0,
