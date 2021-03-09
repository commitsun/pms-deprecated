# Copyright 2021 Dario Lodeiros
# Copyright 2021 Eric Antones
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import fields
from odoo.tools import config

from . import models

if "multi_pms_properties" in config.get("server_wide_modules"):
    _logger = logging.getLogger(__name__)
    _logger.info("monkey patching fields._Relational")

    fields._Relational.check_pms_properties = False
