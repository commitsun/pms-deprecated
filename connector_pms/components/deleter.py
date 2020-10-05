# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent


class PmsChannelConnectorDeleter(AbstractComponent):
    _name = "pms.channel.deleter"
    _inherit = ["base.deleter", "base.pms.channel.connector"]
    _usage = "channel.deleter"
