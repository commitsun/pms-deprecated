import datetime

from freezegun import freeze_time

from .common import TestHotel


class TestPmsFolioSaleLine(TestHotel):
    def create_common_scenario(self):
        # create a room type availability
        self.room_type_availability = self.env[
            "pms.room.type.availability.plan"
        ].create({"name": "Availability plan for TEST"})

        # create a property
        self.property = self.env["pms.property"].create(
            {
                "name": "MY PMS TEST",
                "company_id": self.env.ref("base.main_company").id,
                "default_pricelist_id": self.env.ref("product.list0").id,
            }
        )

        # create room type class
        self.room_type_class = self.env["pms.room.type.class"].create(
            {"name": "Room", "code_class": "ROOM"}
        )

        # create room type
        self.room_type_double = self.env["pms.room.type"].create(
            {
                "pms_property_ids": [self.property.id],
                "name": "Double Test",
                "code_type": "DBL_Test",
                "class_id": self.room_type_class.id,
                "price": 25,
            }
        )
        # create room
        self.room1 = self.env["pms.room"].create(
            {
                "pms_property_id": self.property.id,
                "name": "Double 101",
                "room_type_id": self.room_type_double.id,
                "capacity": 2,
            }
        )

    @freeze_time("1980-11-01")
    def test_compute_folio_sale_lines(self):

        self.create_common_scenario()

        r_test = self.env["pms.reservation"].create(
            {
                "pms_property_id": self.property.id,
                "checkin": datetime.datetime.now(),
                "checkout": datetime.datetime.now() + datetime.timedelta(days=3),
                "adults": 2,
                "room_type_id": self.room_type_double.id,
                "partner_id": self.env.ref("base.res_partner_12").id,
            }
        )
        r_test.flush()

        for _el in self.env["pms.reservation.line"].read_group(
            [("reservation_id", "=", r_test.id)],
            fields=["reservation_id", "price", "discount", "cancel_discount"],
            groupby=["reservation_id", "price", "discount", "cancel_discount"],
            lazy=False,
        ):
            # print(el)
            pass
