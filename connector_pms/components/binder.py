# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class PmsConnectorModelBinder(Component):
    _name = "pms.channel.connector.binder"
    _inherit = ["base.binder", "base.pms.channel.connector"]
    _apply_on = [
        "channel.pms.reservation",
        "channel.pms.room.type",
        "channel.pms.room.type.availability",
        "channel.pms.room.type.restriction",
        "channel.pms.room.type.restriction.item",
        "channel.product.pricelist",
        "channel.product.pricelist.item",
        "channel.ota.info",
    ]
