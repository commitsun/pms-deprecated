# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.component.core import Component


class ProductPricelistImporter(Component):
    _name = "channel.product.pricelist.importer"
    _inherit = "pms.channel.importer"
    _apply_on = ["channel.product.pricelist"]
    _usage = "product.pricelist.importer"

    @api.model
    def import_pricing_plans(self):
        raise NotImplementedError
