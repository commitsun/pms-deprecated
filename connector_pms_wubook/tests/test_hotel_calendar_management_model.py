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
from datetime import timedelta

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.addons.pms import date_utils

from .common import TestPmsWubook


class TestPmsCalendarManagement(TestPmsWubook):
    def test_save_changes(self):
        now_utc_dt = date_utils.now()
        adv_utc_dt = now_utc_dt + timedelta(days=3)
        room_types = (self.pms_room_type_budget,)

        pms_cal_mngt_obj = self.env["pms.calendar.management"].with_user(
            self.user_pms_manager
        )

        # Generate new prices
        prices = (144.0, 170.0, 30.0, 50.0)
        cprices = {}
        for k_item, v_item in enumerate(prices):
            ndate_utc_dt = now_utc_dt + timedelta(days=k_item)
            cprices.setdefault(self.pms_room_type_budget.id, []).append(
                {
                    "date": ndate_utc_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    "price": v_item,
                }
            )

        # Generate new restrictions
        restrictions = {
            "min_stay": (3, 2, 4, 1),
            "max_stay": (5, 8, 9, 3),
            "min_stay_arrival": (2, 3, 6, 2),
            "max_stay_arrival": (4, 7, 7, 4),
            "closed_departure": (False, True, False, True),
            "closed_arrival": (True, False, False, False),
            "closed": (False, False, True, True),
        }
        crestrictions = {}
        for i in range(0, 4):
            ndate_utc_dt = now_utc_dt + timedelta(days=i)
            crestrictions.setdefault(self.pms_room_type_budget.id, []).append(
                {
                    "date": ndate_utc_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    "closed_arrival": restrictions["closed_arrival"][i],
                    "max_stay": restrictions["max_stay"][i],
                    "min_stay": restrictions["min_stay"][i],
                    "closed_departure": restrictions["closed_departure"][i],
                    "closed": restrictions["closed"][i],
                    "min_stay_arrival": restrictions["min_stay_arrival"][i],
                    "max_stay_arrival": restrictions["max_stay_arrival"][i],
                }
            )

        # Generate new availability
        avails = (1, 2, 2, 1)
        cavails = {}
        for k_item, v_item in enumerate(avails):
            ndate_utc_dt = now_utc_dt + timedelta(days=k_item)
            ndate_dt = date_utils.dt_as_timezone(ndate_utc_dt, self.tz_hotel)
            cavails.setdefault(self.pms_room_type_budget.id, []).append(
                {
                    "date": ndate_dt.strftime(DEFAULT_SERVER_DATE_FORMAT),
                    "avail": v_item,
                    "no_ota": False,
                }
            )

        # Save new values
        pms_cal_mngt_obj.save_changes(
            self.default_pricelist_id,
            self.default_restriction_id,
            cprices,
            crestrictions,
            cavails,
        )

        # Check data integrity
        hcal_data = pms_cal_mngt_obj.get_hcalendar_all_data(
            now_utc_dt.strftime(DEFAULT_SERVER_DATE_FORMAT),
            adv_utc_dt.strftime(DEFAULT_SERVER_DATE_FORMAT),
            self.default_pricelist_id,
            self.default_restriction_id,
            True,
        )

        for room_type in room_types:
            for k_pr, v_pr in hcal_data["availability"].items():
                if k_pr == room_type.id:  # Only Check Test Cases
                    for k_info, v_info in enumerate(v_pr):
                        self.assertEqual(
                            v_info["avail"],
                            avails[k_info],
                            "Pms Calendar Management \
                                                Availability doesn't match!",
                        )
            for k_pr, v_pr in hcal_data["restrictions"].items():
                if k_pr == room_type.id:  # Only Check Test Cases
                    for k_info, v_info in enumerate(v_pr):
                        self.assertEqual(
                            v_info["min_stay"],
                            restrictions["min_stay"][k_info],
                            "Pms Calendar Management \
                                                Restrictions doesn't match!",
                        )
                        self.assertEqual(
                            v_info["max_stay"],
                            restrictions["max_stay"][k_info],
                            "Pms Calendar Management \
                                                Restrictions doesn't match!",
                        )
                        self.assertEqual(
                            v_info["min_stay_arrival"],
                            restrictions["min_stay_arrival"][k_info],
                            "Pms Calendar Management Restrictions \
                                                            doesn't match!",
                        )
                        self.assertEqual(
                            v_info["max_stay_arrival"],
                            restrictions["max_stay_arrival"][k_info],
                            "Pms Calendar Management Restrictions \
                                                            doesn't match!",
                        )
                        self.assertEqual(
                            v_info["closed_departure"],
                            restrictions["closed_departure"][k_info],
                            "Pms Calendar Management Restrictions \
                                                            doesn't match!",
                        )
                        self.assertEqual(
                            v_info["closed_arrival"],
                            restrictions["closed_arrival"][k_info],
                            "Pms Calendar Management Restrictions \
                                                            doesn't match!",
                        )
                        self.assertEqual(
                            v_info["closed"],
                            restrictions["closed"][k_info],
                            "Pms Calendar Management Restrictions \
                                                            doesn't match!",
                        )
            for k_pr, v_pr in hcal_data["prices"].items():
                if k_pr == room_type.id:  # Only Check Test Cases
                    for k_info, v_info in enumerate(v_pr):
                        self.assertEqual(
                            v_info["price"],
                            prices[k_info],
                            "Pms Calendar \
                                            Management Prices doesn't match!",
                        )
