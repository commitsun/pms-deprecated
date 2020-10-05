# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent


class PmsChannelConnectorExporter(AbstractComponent):
    _name = "pms.channel.exporter"
    _inherit = ["base.exporter", "base.pms.channel.connector"]
    _usage = "channel.exporter"
