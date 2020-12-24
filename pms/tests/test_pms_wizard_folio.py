# import datetime
# from freezegun import freeze_time
#
import datetime

from freezegun import freeze_time

from odoo import fields

from .common import TestHotel


@freeze_time("1980-12-01")
class TestPmsWizardMassiveChanges(TestHotel):
    def create_common_scenario(self):
        # PRICELIST CREATION
        self.test_pricelist = self.env["product.pricelist"].create(
            {
                "name": "test pricelist 1",
            }
        )
        # AVAILABILITY PLAN CREATION
        self.test_availability_plan = self.env[
            "pms.room.type.availability.plan"
        ].create(
            {
                "name": "Availability plan for TEST",
                "pms_pricelist_ids": [(6, 0, [self.test_pricelist.id])],
            }
        )
        # PROPERTY CREATION (WITH DEFAULT PRICELIST AND AVAILABILITY PLAN
        self.test_property = self.env["pms.property"].create(
            {
                "name": "MY PMS TEST",
                "company_id": self.env.ref("base.main_company").id,
                "default_pricelist_id": self.test_pricelist.id,
                "default_availability_plan_id": self.test_availability_plan.id,
            }
        )
        # CREATION OF ROOM TYPE CLASS
        self.test_room_type_class = self.env["pms.room.type.class"].create(
            {"name": "Room"}
        )

        # CREATION OF ROOM TYPE (WITH ROOM TYPE CLASS)
        self.test_room_type_single = self.env["pms.room.type"].create(
            {
                "pms_property_ids": [self.test_property.id],
                "name": "Single Test",
                "code_type": "SNG_Test",
                "class_id": self.test_room_type_class.id,
            }
        )

        # CREATION OF ROOM TYPE (WITH ROOM TYPE CLASS)
        self.test_room_type_double = self.env["pms.room.type"].create(
            {
                "pms_property_ids": [self.test_property.id],
                "name": "Double Test",
                "code_type": "DBL_Test",
                "class_id": self.test_room_type_class.id,
            }
        )

        # pms.room
        self.test_room1_double = self.env["pms.room"].create(
            {
                "pms_property_id": self.test_property.id,
                "name": "Double 201 test",
                "room_type_id": self.test_room_type_double.id,
                "capacity": 2,
            }
        )
        # pms.room
        self.test_room2_double = self.env["pms.room"].create(
            {
                "pms_property_id": self.test_property.id,
                "name": "Double 202 test",
                "room_type_id": self.test_room_type_double.id,
                "capacity": 2,
            }
        )
        # pms.room
        self.test_room3_double = self.env["pms.room"].create(
            {
                "pms_property_id": self.test_property.id,
                "name": "Double 203 test",
                "room_type_id": self.test_room_type_double.id,
                "capacity": 2,
            }
        )
        # pms.room
        self.test_room4_double = self.env["pms.room"].create(
            {
                "pms_property_id": self.test_property.id,
                "name": "Double 204 test",
                "room_type_id": self.test_room_type_double.id,
                "capacity": 2,
            }
        )
        self.test_room1_single = self.env["pms.room"].create(
            {
                "pms_property_id": self.test_property.id,
                "name": "Single 101 test",
                "room_type_id": self.test_room_type_single.id,
                "capacity": 1,
            }
        )
        # pms.room
        self.test_room2_single = self.env["pms.room"].create(
            {
                "pms_property_id": self.test_property.id,
                "name": "Single 102 test",
                "room_type_id": self.test_room_type_single.id,
                "capacity": 1,
            }
        )

    def test_compute_availability(self):
        # TEST CASE
        # there's availabity for 3 days on test rooms
        # product.pricelist

        # ARRANGE

        # common scenario
        self.create_common_scenario()

        # period to be tested
        checkin = fields.date.today()
        checkout = fields.date.today() + datetime.timedelta(days=5)

        # massive changes for the test
        self.env["pms.massive.changes.wizard"].create(
            {
                "massive_changes_on": "pricelist",
                "pricelist_id": self.test_pricelist.id,
                "start_date": checkin,
                "end_date": checkout,
                "room_type_id": self.test_room_type_double.id,
                "price": 14.50,
                "min_quantity": 1,
            }
        ).apply_massive_changes()

        # force folio wizard to check availability & pricelist results
        wizard = self.env["pms.folio.wizard"].create(
            {
                "start_date": checkin,
                "end_date": checkout,
                "pricelist_id": self.test_pricelist.id,
            }
        )
        wizard.flush()
        for item in wizard.availability_results:
            print(
                "ROOM TYPE->",
                item.room_type_description,
                "| NUM. ROOMS AVAIL.->",
                item.num_rooms_available,
                "| PRICE PER ROOM->",
                item.price_per_room,
            )
        print(wizard.total_price)

        # wizard.availability_results should be:
        # 1. wizard.rooms_available = 4
        #  . wizard.room_type_description = Double Test
        # 2. wizard.rooms_available = 2
        #  . wizard.room_type_description = Single Test

        print(8)
        a = self.env["pms.room.type.availability.plan"].rooms_available(
            fields.date.today(), fields.date.today() + datetime.timedelta(days=3)
        )
        print(a)
