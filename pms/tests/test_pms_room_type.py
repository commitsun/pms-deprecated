# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestRoomType(SavepointCase):
    def setUp(self):
        super().setUp()
        self.p1 = self.browse_ref("pms.main_pms_property")
        self.m1 = self.p1.company_id
        self.folio_sequence = self.env["ir.sequence"].create(
            {
                "name": "PMS Folio",
                "code": "pms.folio",
                "padding": 4,
                "company_id": self.m1.id,
            }
        )
        self.reservation_sequence = self.env["ir.sequence"].create(
            {
                "name": "PMS Reservation",
                "code": "pms.reservation",
                "padding": 4,
                "company_id": self.m1.id,
            }
        )
        self.checkin_sequence = self.env["ir.sequence"].create(
            {
                "name": "PMS Checkin",
                "code": "pms.checkin.partner",
                "padding": 4,
                "company_id": self.m1.id,
            }
        )
        self.p2 = self.env["pms.property"].create(
            {
                "name": "p2",
                "company_id": self.m1.id,
                "default_pricelist_id": self.ref("product.list0"),
                "folio_sequence_id": self.folio_sequence.id,
                "reservation_sequence_id": self.reservation_sequence.id,
                "checkin_sequence_id": self.checkin_sequence.id,
            }
        )
        self.m2 = self.env["res.company"].create(
            {
                "name": "Company m2",
            }
        )
        self.folio_sequence2 = self.env["ir.sequence"].create(
            {
                "name": "PMS Folio",
                "code": "pms.folio",
                "padding": 4,
                "company_id": self.m2.id,
            }
        )
        self.reservation_sequence2 = self.env["ir.sequence"].create(
            {
                "name": "PMS Reservation",
                "code": "pms.reservation",
                "padding": 4,
                "company_id": self.m2.id,
            }
        )
        self.checkin_sequence2 = self.env["ir.sequence"].create(
            {
                "name": "PMS Checkin",
                "code": "pms.checkin.partner",
                "padding": 4,
                "company_id": self.m2.id,
            }
        )
        self.p3 = self.env["pms.property"].create(
            {
                "name": "p3",
                "company_id": self.m2.id,
                "default_pricelist_id": self.ref("product.list0"),
                "folio_sequence_id": self.folio_sequence2.id,
                "reservation_sequence_id": self.reservation_sequence2.id,
                "checkin_sequence_id": self.checkin_sequence2.id,
            }
        )
        self.p4 = self.env["pms.property"].create(
            {
                "name": "p4",
                "company_id": self.m2.id,
                "default_pricelist_id": self.ref("product.list0"),
                "folio_sequence_id": self.folio_sequence2.id,
                "reservation_sequence_id": self.reservation_sequence2.id,
                "checkin_sequence_id": self.checkin_sequence2.id,
            }
        )


class TestRoomTypeCodePropertyIntegrity(TestRoomType):
    # internal integrity
    def test_internal_case_01(self):
        """
        PRE:    - room type r1 does not exists
        ACT:    - create a new r1 room
                - r1 has code c1
                - r1 has property p1
                - p1 has company m1
                - r1 has company m1
        POST:   - r1 created
        """
        # ARRANGE & ACT & ASSERT
        try:
            # r1
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id])],
                    "company_id": self.m1.id,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )
        except ValidationError:
            self.fail("Room type not created when it should")

    def test_internal_case_02(self):
        """
        PRE:    - room type r1 does not exists
        ACT:    - create a new r1 room
                - r1 has code c1
                - r1 has property p1
                - p1 has company m1
                - r1 has company m2
        POST:   - Integrity error, p1 has company m1 and room type m2
                - r1 not created
        """
        # ARRANGE & ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The room type has been created and it shouldn't"
        ):
            # r1
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id])],
                    "company_id": self.m2.id,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )

    def test_internal_case_03(self):
        """
        PRE:    - room type r1 does not exists
        ACT:    - create a new r1 room
                - r1 has code c1
                - r1 has property p1 and p3
                - p1 has company m1
                - p3 has company m2
                - r1 has company m2
        POST:   - Integrity error, p1 has company m1 and room type m2
                - r1 not created
        """
        # ARRANGE & ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The room type has been created and it shouldn't"
        ):
            # r1
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id, self.p3.id])],
                    "company_id": self.m2.id,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )

    def test_internal_case_04(self):
        """
        PRE:    - room type r1 does not exists
        ACT:    - create a new r1 room
                - r1 has code c1
                - r1 has property p1 and p3
                - p1 has company m1
                - p3 has company m2
                - r1 has no company
        POST:   - r1 created
        """
        # ARRANGE & ACT & ASSERT
        try:
            # r1
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id, self.p3.id])],
                    "company_id": False,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )
        except ValidationError:
            self.fail("Room type not created when it should")

    # external integrity
    def test_external_case_01(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 has company m1
                - r1 has no company
        ACT:    - create a new r2 room
                - r2 has code c1
                - r2 has property p1
                - p1 has company m1
                - r2 has no company
        POST:   - Integrity error: the room type already exists
                - r2 not created
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The room type has been created and it shouldn't"
        ):
            # r2
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id])],
                    "company_id": False,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )

    def test_external_case_02(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 has company m1
                - r1 has no company
        ACT:    - create a new r2 room
                - r2 has code c1
                - r2 has property p1
                - p1 has company m1
                - r2 has company m1
        POST:   - Integrity error: the room type already exists
                - r2 not created
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The room type has been created and it shouldn't"
        ):
            # r2
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id])],
                    "company_id": self.m1.id,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )

    def test_external_case_03(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 has company m1
                - r1 has company m1
        ACT:    - create a new r2 room
                - r2 has code c1
                - r2 has property p1, p2, p3
                - p1, p2 has company m1
                - p3 has company m2
                - r2 has no company
        POST:   - Integrity error: the room type already exists
                - r2 not created
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": self.m1.id,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The room type has been created and it shouldn't"
        ):
            # r2
            self.env["pms.room.type"].create(
                {
                    "name": "Room type r1",
                    "default_code": "c1",
                    "pms_property_ids": [(6, 0, [self.p1.id, self.p2.id, self.p3.id])],
                    "company_id": False,
                    "class_id": self.ref("pms.pms_room_type_class_0"),
                }
            )


class TestRoomTypeCodePropertyUniqueness(TestRoomType):
    # test with one room type
    def test_single_case_01(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 with 2 properties p1 and p2
                - p1 and p2 have the same company m1
                - r1 has no company
        ACT:    - search room type with code c1 and property p1
                - p1 has company m1
        POST:   - only r1 room type found
        """
        # ARRANGE
        r1 = self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id, self.p3.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p1.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r1.id, "Expected room type not found")

    def test_single_case_02(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 with 2 properties p1 and p3
                - p1 and p2 have differmt companies
                - p1 have company m1 and p3 have company m2
                - r1 has no company
        ACT:    - search room type with code c1 and property p1
                - p1 has company m1
        POST:   - only r1 room type found
        """
        # ARRANGE
        r1 = self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id, self.p3.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p1.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r1.id, "Expected room type not found")

    def test_single_case_03(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 with 2 properties p1 and p2
                - p1 and p2 have same company m1
                - r1 has no company
        ACT:    - search room type with code c1 and property p3
                - p3 have company m2
        POST:   - no room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id, self.p2.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p3.id, "c1"
        )

        # ASSERT
        self.assertFalse(room_type, "Room type found but it should have not found any")

    def test_single_case_04(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 properties are null
                - r1 company is m1
        ACT:    - search room type with code c1 and property p1
                - p1 have company m1
        POST:   - only r1 room type found
        """
        # ARRANGE
        r1 = self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": self.m1.id,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p1.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r1.id, "Expected room type not found")

    def test_single_case_05(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 properties are null
                - r1 company is m1
        ACT:    - search room type with code c1 and property p3
                - p3 have company m2
        POST:   - no room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": self.m1.id,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p3.id, "c1"
        )

        # ASSERT
        self.assertFalse(room_type, "Room type found but it should have not found any")

    # tests with more than one room type
    def test_multiple_case_01(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 with 2 properties p1 and p2
                - p1 and p2 have the same company m1
                - r1 has no company
                - room type r2 exists
                - r2 has code c1
                - r2 has no properties
                - r2 has no company
        ACT:    - search room type with code c1 and property p1
                - p1 have company m1
        POST:   - only r1 room type found
        """
        # ARRANGE
        r1 = self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id, self.p3.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        # r2
        self.env["pms.room.type"].create(
            {
                "name": "Room type r2",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p1.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r1.id, "Expected room type not found")

    def test_multiple_case_02(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 have the company m1
                - r1 has no company
                - room type r2 exists
                - r2 has code c1
                - r2 has no properties
                - r2 has no company
        ACT:    - search room type with code c1 and property p2
                - p2 have company m1
        POST:   - only r1 room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        r2 = self.env["pms.room.type"].create(
            {
                "name": "Room type r2",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p2.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r2.id, "Expected room type not found")

    def test_multiple_case_03(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 have the company m1
                - r1 has no company
                - room type r2 exists
                - r2 has code c1
                - r2 has no properties
                - r2 has no company
        ACT:    - search room type with code c1 and property p3
                - p3 have company m2
        POST:   - only r2 room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        r2 = self.env["pms.room.type"].create(
            {
                "name": "Room type r2",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p3.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r2.id, "Expected room type not found")

    def test_multiple_case_04(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 have the company m1
                - r1 has no company
                - room type r2 exists
                - r2 has code c1
                - r2 has no properties
                - r2 has company m1
        ACT:    - search room type with code c1 and property p3
                - p3 have company m2
        POST:   - no room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        # r2
        self.env["pms.room.type"].create(
            {
                "name": "Room type r2",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": self.m1.id,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p3.id, "c1"
        )

        # ASSERT
        self.assertFalse(room_type, "Room type found but it should have not found any")

    def test_multiple_case_05(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 have the company m1
                - r1 has no company
                - room type r2 exists
                - r2 has code c1
                - r2 has no properties
                - r2 has company m2
        ACT:    - search room type with code c1 and property p3
                - p3 have company m2
        POST:   - r2 room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        r2 = self.env["pms.room.type"].create(
            {
                "name": "Room type r2",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": self.m2.id,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p3.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r2.id, "Expected room type not found")

    def test_multiple_case_06(self):
        """
        PRE:    - room type r1 exists
                - r1 has code c1
                - r1 has property p1
                - p1 have the company m1
                - r1 has no company
                - room type r2 exists
                - r2 has code c1
                - r2 has no properties
                - r2 has company m1
                - room type r3 exists
                - r3 has code c1
                - r3 has no properties
                - r3 has no company
        ACT:    - search room type with code c1 and property p3
                - p3 have company m2
        POST:   - r3 room type found
        """
        # ARRANGE
        # r1
        self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "default_code": "c1",
                "pms_property_ids": [(6, 0, [self.p1.id])],
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        # r2
        self.env["pms.room.type"].create(
            {
                "name": "Room type r2",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": self.m1.id,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )
        r3 = self.env["pms.room.type"].create(
            {
                "name": "Room type r3",
                "default_code": "c1",
                "pms_property_ids": False,
                "company_id": False,
                "class_id": self.ref("pms.pms_room_type_class_0"),
            }
        )

        # ACT
        room_type = self.env["pms.room.type"].get_room_types_by_property(
            self.p3.id, "c1"
        )

        # ASSERT
        self.assertEqual(room_type.id, r3.id, "Expected room type not found")

    def test_check_property_room_type_class(self):
        # ARRANGE
        room_type_class = self.env["pms.room.type.class"].create(
            {
                "name": "Room Type Class",
                "code_class": "ROOM",
                "pms_property_ids": [
                    (4, self.p2.id),
                ],
            },
        )
        # ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="Room Type has been created and it shouldn't"
        ):
            r = self.env["pms.room.type"].create(
                {
                    "name": "Room Type",
                    "default_code": "c1",
                    "class_id": room_type_class.id,
                    "pms_property_ids": [
                        (4, self.p2.id),
                    ],
                }
            )
            r.pms_property_ids = [(4, self.p1.id)]

    # TODO: pending multi property PR
    #def test_check_board_service_property_integrity(self):

    #    self.room_type_class = self.env["pms.room.type.class"].create(
     #       {"name": "Room Type Class", "code_class": "SIN1"}
      #  )
      #  self.room_type = self.env["pms.room.type"].create(
       #     {
       #         "name": "Room Type",
        #        "default_code": "Type1",
       #         "pms_property_ids": self.p3,
       #         "class_id": self.room_type_class.id,
       #     }
       # )
       # self.board_service = self.env["pms.board.service"].create(
       #     {
       #         "name": "Board Service",
       #     }
       # )
       # with self.assertRaises(ValidationError):
       #     self.env["pms.board.service.room.type"].create(
       #         {
       #             "pms_board_service_id": self.board_service.id,
       #             "pms_room_type_id": self.room_type.id,
       #             "pricelist_id": self.env.ref("product.list0").id,
       #             "pms_property_ids": self.p4,
       #         }
       #     )

    def test_check_amenities_property_integrity(self):
        self.amenity = self.env["pms.amenity"].create(
            {"name": "Amenity", "pms_property_ids": self.p3}
        )
        self.room_type_class = self.env["pms.room.type.class"].create(
            {"name": "Room Type Class", "code_class": "SIN1"}
        )
        with self.assertRaises(ValidationError):
            self.env["pms.room.type"].create(
                {
                    "name": "Room Type",
                    "default_code": "Type1",
                    "class_id": self.room_type_class.id,
                    "pms_property_ids": [self.p4.id],
                    "room_amenity_ids": [self.amenity.id],
                }
            )
