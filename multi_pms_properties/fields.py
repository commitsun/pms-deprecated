# © 2020  Dario Lodeiros
# © 2020  Eric Antones
import logging

from odoo.fields import _Relational

# class RelationalCustom(_Relational):

_logger = logging.getLogger(__name__)
_logger.info("monkey patching multi properties check")
_Relational.check_pms_properties = False
