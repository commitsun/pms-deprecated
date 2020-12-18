import datetime

from freezegun import freeze_time

from odoo import fields

from .common import TestHotel


class TestPmsReservations(TestHotel):
    def create_common_scenario(self):
        # product.pricelist
        self.test_pricelist = self.env["product.pricelist"].create(
            {
                "name": "test pricelist 1",
            }
        )
        # pms.room.type.availability.plan
        self.test_availability_plan = self.env["pms.room.type.availability.plan"].create(
            {
                "name": "Availability plan for TEST",
                "pms_pricelist_ids": [(6, 0, [self.test_pricelist.id])],
            }
        )
        # pms.property
        self.test_property = self.env["pms.property"].create(
            {
                "name": "MY PMS TEST",
                "company_id": self.env.ref("base.main_company").id,
                "default_pricelist_id": self.test_pricelist.id,
                "default_availability_plan_id": self.test_availability_plan.id,
            }
        )
        # pms.room.type.class
        self.test_room_type_class = self.env["pms.room.type.class"].create(
            {"name": "Room"}
        )

        # pms.room.type
        self.test_room_type_single = self.env["pms.room.type"].create(
            {
                "pms_property_ids": [self.test_property.id],
                "name": "Single Test",
                "code_type": "SNG_Test",
                "class_id": self.test_room_type_class.id,
            }
        )
        # pms.room.type
        self.test_room_type_double = self.env["pms.room.type"].create(
            {
                "pms_property_ids": [self.test_property.id],
                "name": "Double Test",
                "code_type": "DBL_Test",
                "class_id": self.test_room_type_class.id,
            }
        )

    @freeze_time("1980-12-01")
    def test_num_rules_on_create01(self):

        # TEST CASE
        # rules for 1,2,3,4 days

        # ARRANGE
        self.create_common_scenario()

        for days in [0, 1, 2, 3]:
            with self.subTest(k=days):
                num_exp_rules_to_create = days + 1

                self.env["pms.massive.changes.wizard"].create(
                    {
                        "availability_plan_id": self.test_availability_plan.id,
                        "start_date": fields.date.today(),
                        "end_date": fields.date.today() + datetime.timedelta(days=days),
                        "room_type_id": self.test_room_type_double.id,
                    }
                ).apply_availability_rules()

                self.assertEqual(
                    len(self.test_availability_plan.rule_ids),
                    num_exp_rules_to_create,
                    "the number of rules created by the wizard should include all the "
                    "days between start and finish (both included)",
                )

    @freeze_time("1980-12-01")
    def test_num_rules_on_create_no_room_type(self):
        # TEST CASE
        # rules for 3 days and no room type is applied

        # ARRANGE
        self.create_common_scenario()
        date_from = fields.date.today()
        date_to = fields.date.today() + datetime.timedelta(days=3)

        num_room_types = self.env["pms.room.type"].search_count([])
        num_exp_rules_to_create = ((date_to - date_from).days + 1) * num_room_types

        # ACT
        self.env["pms.massive.changes.wizard"].create(
            {
                "availability_plan_id": self.test_availability_plan.id,
                "start_date": date_from,
                "end_date": date_to,
            }
        ).apply_availability_rules()

        # ASSERT
        self.assertEqual(
            len(self.test_availability_plan.rule_ids),
            num_exp_rules_to_create,
            "the number of rules created by the wizard should consider all "
            "room types when one is not applied",
        )

    @freeze_time("1980-12-01")
    def test_avail_rules_on_create_one_rule(self):
        # TEST CASE
        # check all the rule's values

        # ARRANGE
        self.create_common_scenario()
        date_from = fields.date.today()
        date_to = fields.date.today()

        vals = {
            "availability_plan_id": self.test_availability_plan.id,
            "start_date": date_from,
            "end_date": date_to,
            "room_type_id": self.test_room_type_double.id,
            "quota": 50,
            "max_avail": 5,
            "min_stay": 10,
            "min_stay_arrival": 10,
            "max_stay": 10,
            "max_stay_arrival": 10,
            "closed": True,
            "closed_arrival": True,
            "closed_departure": True,
        }

        # ACT
        self.env["pms.massive.changes.wizard"].create(vals).apply_availability_rules()

        # ASSERT
        del vals["availability_plan_id"]
        del vals["start_date"]
        del vals["end_date"]
        del vals["room_type_id"]
        for key in vals:
            with self.subTest(k=key):
                self.assertEqual(
                    self.test_availability_plan.rule_ids[0][key],
                    vals[key],
                    "The value of " + key + " is not correctly established",
                )

    @freeze_time("1980-12-01")
    def test_avail_rules_on_create_days_of_week(self):
        # TEST CASE
        # check all the rule's values for days of week are created

        # ARRANGE
        self.create_common_scenario()
        test_case_week_days = [
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ]

        date_from = fields.date.today()
        date_to = fields.date.today() + datetime.timedelta(days=6)

        wizard = self.env["pms.massive.changes.wizard"].create(
            {
                "availability_plan_id": self.test_availability_plan.id,
                "room_type_id": self.test_room_type_double.id,
                "start_date": date_from,
                "end_date": date_to,
            }
        )

        for index, test_case in enumerate(test_case_week_days):
            with self.subTest(k=test_case):
                # ARRANGE
                wizard.write(
                    {
                        "apply_on_monday": test_case[0],
                        "apply_on_tuesday": test_case[1],
                        "apply_on_wednesday": test_case[2],
                        "apply_on_thursday": test_case[3],
                        "apply_on_friday": test_case[4],
                        "apply_on_saturday": test_case[5],
                        "apply_on_sunday": test_case[6],
                    }
                )
                # ACT
                wizard.apply_availability_rules()

                # ASSERT
                self.assertTrue(
                    self.test_availability_plan.rule_ids[index].date.timetuple()[6]
                    == index
                    and test_case[index]
                )
