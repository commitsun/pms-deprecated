import datetime

import pytz

from odoo import api, fields, models


class FolioWizard(models.TransientModel):
    _name = "pms.folio.wizard"
    _description = (
        "Wizard to check availability by room type and pricelist &"
        " creation of folios with its reservations"
    )
    # Fields declaration
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Pricelist to apply massive changes",
    )
    start_date = fields.Date(
        string="From:",
        required=True,
    )
    end_date = fields.Date(
        string="To:",
        required=True,
    )
    availability_results = fields.One2many(
        comodel_name="pms.folio.availability.wizard",
        inverse_name="folio_wizard_id",
        compute="_compute_availability_results",
        store=True,
        readonly=False,
    )
    total_price = fields.Float(string="Total Price", compute="_compute_total_price")
    discount = fields.Float(
        string="Discount",
        default=0,
    )
    partner_id = fields.Many2one(
        "res.partner",
    )
    @api.depends("availability_results", "discount")
    def _compute_total_price(self):
        for record in self:
            record.total_price = 0
            for avail_result in record.availability_results:
                record.total_price += avail_result.price_total
            record.total_price = record.total_price * (1 - record.discount)

    @api.depends(
        "start_date",
        "end_date",
        "pricelist_id",
    )
    def _compute_availability_results(self):

        tz = "Europe/Madrid"

        for record in self:

            record.availability_results = False

            if record.start_date and record.end_date and record.pricelist_id:

                cmds = [(5, 0, 0)]
                for room_type in self.env["pms.room.type"].search([]):
                    num_rooms_available_by_date = []

                    room_type_total_price = 0
                    for date in [
                        record.start_date + datetime.timedelta(days=x)
                        for x in range(
                            0, (record.end_date - record.start_date).days + 1
                        )
                    ]:
                        rooms_available = self.env[
                            "pms.room.type.availability.plan"
                        ].rooms_available(
                            date,
                            date + datetime.timedelta(days=1),
                            room_type_id=room_type.id,
                            pricelist=record.pricelist_id.id,
                        )

                        num_rooms_available_by_date.append(len(rooms_available))

                        dt_from = datetime.datetime.combine(
                            date,
                            datetime.time.min,
                        )
                        dt_to = datetime.datetime.combine(
                            date,
                            datetime.time.max,
                        )
                        dt_from = pytz.timezone(tz).localize(dt_from)
                        dt_to = pytz.timezone(tz).localize(dt_to)
                        dt_from = dt_from.astimezone(pytz.utc)
                        dt_to = dt_to.astimezone(pytz.utc)
                        dt_from = dt_from.replace(tzinfo=None)
                        dt_to = dt_to.replace(tzinfo=None)
                        pricelist_item = self.env["product.pricelist.item"].search(
                            [
                                ("pricelist_id", "=", record.pricelist_id.id),
                                ("date_start", ">=", dt_from),
                                ("date_end", "<=", dt_to),
                                ("applied_on", "=", "1_product"),
                                (
                                    "product_tmpl_id",
                                    "=",
                                    room_type.product_id.product_tmpl_id.id,
                                ),
                            ]
                        )

                        if pricelist_item:
                            pricelist_item.ensure_one()
                            room_type_total_price += float(pricelist_item.price[2:])
                        else:
                            room_type_total_price += room_type.product_id.list_price
                    if room_type.total_rooms_count > 0:
                        cmds.append(
                            (
                                0,
                                0,
                                {
                                    "folio_wizard_id": record.id,
                                    "room_type_id": room_type.id,
                                    "num_rooms_available": min(
                                        num_rooms_available_by_date
                                    ),
                                    "price_per_room": room_type_total_price
                                    if min(num_rooms_available_by_date) > 0
                                    else 0,
                                },
                            )
                        )
                record.availability_results = cmds
                record.availability_results = record.availability_results.sorted(
                    key=lambda s: s.num_rooms_available
                )


    # actions
    def create_folio(self):
        for record in self:

            folio = self.env["pms.folio"].create(
                {
                    "pricelist_id": record.pricelist_id.id,
                    "partner_id": record.partner_id.id,
                }
            )
            record.invalidate_cache()


            for line in record.availability_results:
                print(line.value_num_rooms_selected)


                for reservations_to_create in range(0, line.value_num_rooms_selected):
                    print('create')
                    self.env['pms.reservation'].create(
                        {
                            'folio_id': folio.id,
                            'checkin': record.start_date,
                            'checkout': record.end_date,
                            'room_type_id': line.room_type_id.id,
                            'partner_id': folio.partner_id.id,
                            "pricelist_id": record.pricelist_id.id,
                        }
                    )
