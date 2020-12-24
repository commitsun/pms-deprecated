from odoo import api, fields, models


class DatesWizard(models.TransientModel):

    _name = "pms.filter.dates.wizard"
    _description = "Wizard for filter by dates"

    search_models = fields.Selection(
        [
            ("reservation", "Reservation"),
            ("checkins", "Checkins"),
            ("services", "Services"),
            ("folios", "Folios"),
            ("invoices", "Invoices"),
            ("payments", "Payments"),
        ],
        string="Models",
        default="reservation",
        required=True,
    )
    reservation_ids = fields.One2many(
        comodel_name="pms.reservation",
        string="Filtered reservations",
        compute="_compute_reservation_dates",
    )
    checkin_partner_ids = fields.One2many(
        comodel_name="pms.checkin.partner",
        string="Filtered checkin partners",
        compute="_compute_checkin_partner_dates",
    )
    services_ids = fields.One2many(
        comodel_name="pms.service.line",
        string="Filtered services",
        compute="_compute_services_dates",
    )
    folio_ids = fields.One2many(
        comodel_name="pms.folio",
        string="Filtered folios",
        compute="_compute_folios_dates",
    )
    invoice_ids = fields.One2many(
        comodel_name="account.invoice.report",
        string="Filtered invoices",
        compute="_compute_invoices_dates",
    )
    invoice_dates_fields = fields.Selection(
        [("invoice_date", "Invoice date"), ("invoice_due_date", "Due date")],
        string="Invoice Dates",
        default="invoice_date",
        required=True,
    )
    payments_ids = fields.One2many(
        comodel_name="account.payment",
        string="Filtered payments",
        compute="_compute_payments_dates",
    )
    date_start = fields.Date(string="Date start", required=True)
    date_end = fields.Date(string="Date End", required=True)

    @api.depends("search_models", "date_start", "date_end")
    def _compute_reservation_dates(self):
        for record in self:
            if (
                record.search_models == "reservation"
                and record.date_start
                and record.date_end
            ):
                reservations = self.env["pms.reservation"].search(
                    [
                        ("checkin", ">=", record.date_start),
                        ("checkout", "<=", record.date_end),
                    ]
                )
                record.reservation_ids = reservations
            else:
                record.reservation_ids = False

    @api.depends("search_models", "date_start", "date_end")
    def _compute_checkin_partner_dates(self):
        for record in self:
            if (
                record.search_models == "checkins"
                and record.date_start
                and record.date_end
            ):
                checkin_partners = self.env["pms.checkin.partner"].search(
                    [
                        ("arrival", ">=", record.date_start),
                        ("arrival", "<=", record.date_end),
                    ]
                )
                record.checkin_partner_ids = checkin_partners
            else:
                record.checkin_partner_ids = False

    @api.depends("search_models", "date_start", "date_end")
    def _compute_services_dates(self):
        for record in self:
            if (
                record.search_models == "services"
                and record.date_start
                and record.date_end
            ):
                services = self.env["pms.service.line"].search(
                    [("date", ">=", record.date_start), ("date", "<=", record.date_end)]
                )
                record.services_ids = services
            else:
                record.services_ids = False

    @api.depends("search_models", "date_start", "date_end")
    def _compute_folios_dates(self):
        for record in self:
            if (
                record.search_models == "folios"
                and record.date_start
                and record.date_end
            ):
                folios = self.env["pms.folio"].search(
                    [
                        ("date_order", ">=", record.date_start),
                        ("date_order", "<=", record.date_end),
                    ]
                )
                record.folio_ids = folios
            else:
                record.folio_ids = False

    @api.depends("search_models", "date_start", "date_end")
    def _compute_invoice_dates(self):
        for record in self:
            if (
                record.search_models == "invoices"
                and record.date_start
                and record.date_end
            ):
                if record.invoice_dates_fields == "invoice_date":
                    invoices = self.env["account.invoice.report"].search(
                        [
                            ("invoice_date", ">=", record.date_start),
                            ("invoice_date", "<=", record.date_end),
                        ]
                    )
                if record.invoice_dates_fields == "invoice_due_date":
                    invoices = self.env["account.invoice.report"].search(
                        [
                            ("invoice_date_due", ">=", record.date_start),
                            ("invoice_date_due", "<=", record.date_end),
                        ]
                    )
                record.invoice_ids = invoices
            else:
                record.invoice_ids = False

    @api.depends("search_models", "date_start", "date_end")
    def _compute_payments_dates(self):
        for record in self:
            if (
                record.search_models == "payments"
                and record.date_start
                and record.date_end
            ):
                payments = self.env["account.payment"].search(
                    [("date", ">=", record.date_start), ("date", "<=", record.date_end)]
                )
                record.payments_ids = payments
            else:
                record.payments_ids = False
