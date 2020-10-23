# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ChannelWubookPmsFolioBinding(models.Model):
    _name = "channel.wubook.pms.folio"
    _inherit = "channel.wubook.binding"
    _inherits = {"pms.folio": "odoo_id"}

    # binding fields
    odoo_id = fields.Many2one(
        comodel_name="pms.folio",
        string="Odoo ID",
        required=True,
        ondelete="cascade",
    )

    @api.model
    def import_data(self, backend_id, date_from, date_to, mark):
        """ Prepare the batch import of Folios from Channel """
        domain = []
        if date_from and date_to:
            domain += [
                ("date_arrival", ">=", date_from),
                ("date_arrival", "<=", date_to),
            ]

        return self.import_batch(backend_record=backend_id, domain=domain)

    # def write(self, values):
    #     # workaround to surpass an Odoo bug in a delegation inheritance
    #     # of product.pricelist that does not let to write 'name' field
    #     # if 'items_ids' is written as well on the same write call.
    #     # With other fields like 'sequence' it does not crash but it does not
    #     # save the value entered. For other fields it works but it's unstable.
    #     item_ids = values.pop("item_ids", None)
    #     if item_ids:
    #         super().write({"item_ids": item_ids})
    #     if values:
    #         return super().write(values)
