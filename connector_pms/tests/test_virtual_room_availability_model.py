##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Solucións Aloxa S.L. <info@aloxa.eu>
#                       Alexandre Díaz <dev@redneboa.es>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo.addons.pms import date_utils

from .common import TestPmsWubook


class TestVirtualRoomAvailability(TestPmsWubook):
    def test_write(self):
        now_utc_dt = date_utils.now()
        room_type_avail_obj = self.env["pms.room.type.availability"]
        avail = room_type_avail_obj.search(
            [
                ("room_type_id", "=", self.pms_room_type_budget.id),
                ("date", "=", now_utc_dt.strftime(DEFAULT_SERVER_DATE_FORMAT)),
            ],
            limit=1,
        )
        avail.write({"avail": 1})
        self.assertEqual(avail.avail, 1, "Invalid avail")
