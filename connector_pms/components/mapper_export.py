# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent


class ChannelExportMapper(AbstractComponent):
    _name = "channel.export.mapper"
    _inherit = ["base.hotel.channel.connector", "base.export.mapper"]
    _usage = "export.mapper"
