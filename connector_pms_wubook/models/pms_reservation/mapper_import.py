# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, only_create


class ChannelWubookPmsReservationMapperImport(Component):
    _name = "channel.wubook.pms.reservation.mapper.import"
    _inherit = "channel.wubook.mapper.import"

    _apply_on = "channel.wubook.pms.reservation"

    children = [
        ("lines", "reservation_line_ids", "channel.wubook.pms.reservation.line"),
    ]

    @only_create
    @mapping
    def reservations(self, record):
        values = {
            "pms_property_id": self.backend_record.pms_property_id.id,
            "arrival_hour": record["arrival_hour"],
            "checkin": record["date_arrival"],
            "checkout": record["date_departure"],
            "adults": record["occupancy"],
        }

        rt_binder = self.binder_for("channel.wubook.pms.room.type")
        room_type = rt_binder.to_internal(record["room_id"], unwrap=True)
        assert room_type, (
            "room_id %s should have been imported in "
            "PmsRoomTypeImporter._import_dependencies" % (record["room_id"],)
        )
        values["room_type_id"] = room_type.id

        if record["board"]:
            bd_binder = self.binder_for("channel.wubook.pms.board.service")
            board_service = bd_binder.to_internal(record["board"], unwrap=True)
            assert board_service, (
                "board_service_id '%s' should've been imported in "
                "PmsRoomTypeImporter._import_dependencies.\n"
                "Make sure the Room Type '%s' has that Board Service '%s' "
                "defined in the backend."
                % (record["board"], room_type.default_code, record["board"])
            )
            board_service_room_type_id = room_type.board_service_room_type_ids.filtered(
                lambda x: x.pms_board_service_id == board_service
            )
            if not board_service_room_type_id:
                raise ValidationError(
                    _("The Board Service '%s' is not available in Room Type '%s'")
                    % (board_service.default_code, room_type.default_code)
                )
            elif len(board_service_room_type_id) > 1:
                raise ValidationError(
                    _("The Board Service '%s' is duplicated in Room Type '%s'")
                    % (board_service.default_code, room_type.default_code)
                )
            values["board_service_room_id"] = board_service_room_type_id.id

        # pl_binder = self.binder_for("channel.wubook.product.pricelist")
        # pricelist = pl_binder.to_internal(record["rate_id"], unwrap=True)
        # assert pricelist, (
        #     "rate_id %s should have been imported in "
        #     "ProductPricelistImporter._import_dependencies" % (record['rate_id'],))

        # values["pricelist_id"] = pricelist.id
        # values["pricelist_id"] = self.env.ref('product.list0').id

        # partner_id
        # values["partner_id"] = record.partner_id.id

        return values

    @only_create
    @mapping
    def dates(self, record):
        return {
            "arrival_hour": record["arrival_hour"],
            "checkin": record["date_arrival"],
            "checkout": record["date_departure"],
        }

    @only_create
    @mapping
    def requests(self, record):
        return {
            "partner_requests": record["customer_notes"],
        }

    # ttype = record["type"]
    # if ttype == "pricelist":
    #     pl_binder = self.binder_for("channel.wubook.product.pricelist")
    #     pricelist = pl_binder.to_internal(record["vpid"], unwrap=True)
    #     if not pricelist:
    #         raise ValidationError(
    #             _(
    #                 "External record with id %i not exists. "
    #                 "It should be imported in _import_dependencies"
    #             )
    #             % record["vpid"]
    #         )
    #     values = {
    #         "applied_on": "3_global",
    #         "compute_price": "formula",
    #         "base": "pricelist",
    #         "base_pricelist_id": pricelist.id,
    #     }
    #     variation_type = record["variation_type"]
    #     variation = record["variation"]
    #     if variation_type == -2:
    #         values["price_discount"] = 0
    #         values["price_surcharge"] = -variation
    #     elif variation_type == -1:
    #         values["price_discount"] = variation
    #         values["price_surcharge"] = 0
    #     elif variation_type == 1:
    #         values["price_discount"] = -variation
    #         values["price_surcharge"] = 0
    #     elif variation_type == 2:
    #         values["price_discount"] = 0
    #         values["price_surcharge"] = variation
    #     else:
    #         raise ValidationError(_("Unknown variation type %s") % variation_type)
    # elif ttype == "room":
    #     # TODO
    #     pass
    # else:
    #     raise ValidationError(_("Unknown type '%s'") % ttype)
    # return values


class ChannelWubookPmsReservationChildMapperImport(Component):
    _name = "channel.wubook.pms.reservation.child.mapper.import"
    _inherit = "channel.wubook.child.mapper.import"
    _apply_on = "channel.wubook.pms.reservation.line"

    # def get_item_values(self, map_record, to_attr, options):
    #     values = super().get_item_values(map_record, to_attr, options)
    #     common_keys = {"applied_on", "compute_price"}
    #     if {*common_keys, "base", "base_pricelist_id"}.issubset(values):
    #         binding = options.get("binding")
    #         if binding:
    #             item_ids = binding.item_ids.filtered(
    #                 lambda x: all(
    #                     [
    #                         x.applied_on == values["applied_on"],
    #                         x.compute_price == values["compute_price"],
    #                         x.base == values["base"],
    #                         x.base_pricelist_id.id == values["base_pricelist_id"],
    #                     ]
    #                 )
    #             )
    #             if item_ids:
    #                 if len(item_ids) > 1:
    #                     raise ValidationError(
    #                         _(
    #                             "Found two pricelist items with same properties %s. "
    #                             "Please remove one of them"
    #                         )
    #                         % values
    #                     )
    #                 values["id"] = item_ids.id
    #
    #     return values

    # def format_items(self, items_values):
    #     ops = []
    #     for values in items_values:
    #         _id = values.pop("id", None)
    #         if _id:
    #             ops.append((1, _id, values))
    #         else:
    #             ops.append((0, 0, values))
    #
    #     return ops
