from odoo.exceptions import ValidationError
from odoo.tests import common


class TestPmsAmenity(common.SavepointCase):
    def create_common_scenario(self):
        # Created a company with three properties
        # +-----------+-----------------------------------+
        # | Company | Properties                         |
        # +-----------+-----------------------------------+
        # | Company1 | Property1 - Property2 - Property3 |
        # +-----------+-----------------------------------+

        self.company1 = self.env["res.company"].create(
            {
                "name": "Pms_Company_Test",
            }
        )
        self.folio_sequence = self.env["ir.sequence"].create(
            {
                "name": "PMS Folio",
                "code": "pms.folio",
                "padding": 4,
                "company_id": self.company1.id,
            }
        )
        self.reservation_sequence = self.env["ir.sequence"].create(
            {
                "name": "PMS Reservation",
                "code": "pms.reservation",
                "padding": 4,
                "company_id": self.company1.id,
            }
        )
        self.checkin_sequence = self.env["ir.sequence"].create(
            {
                "name": "PMS Checkin",
                "code": "pms.checkin.partner",
                "padding": 4,
                "company_id": self.company1.id,
            }
        )
        self.property1 = self.env["pms.property"].create(
            {
                "name": "Pms_property_test1",
                "company_id": self.company1.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
                "folio_sequence_id": self.folio_sequence.id,
                "reservation_sequence_id": self.reservation_sequence.id,
                "checkin_sequence_id": self.checkin_sequence.id,
            }
        )
        self.property2 = self.env["pms.property"].create(
            {
                "name": "Pms_property_test2",
                "company_id": self.company1.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
                "folio_sequence_id": self.folio_sequence.id,
                "reservation_sequence_id": self.reservation_sequence.id,
                "checkin_sequence_id": self.checkin_sequence.id,
            }
        )

        self.property3 = self.env["pms.property"].create(
            {
                "name": "Pms_property_test3",
                "company_id": self.company1.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
                "folio_sequence_id": self.folio_sequence.id,
                "reservation_sequence_id": self.reservation_sequence.id,
                "checkin_sequence_id": self.checkin_sequence.id,
            }
        )

    def test_property_not_allowed(self):
        # Creation of a Amenity with Properties incompatible with it Amenity Type

        # +-----------------------------------+-----------------------------------+
        # |  Amenity Type (TestAmenityType1)  |      Amenity (TestAmenity1)       |
        # +-----------------------------------+-----------------------------------+
        # |      Property1 - Property2        | Property1 - Property2 - Property3 |
        # +-----------------------------------+-----------------------------------+

        # ARRANGE
        self.create_common_scenario()
        AmenityType = self.env["pms.amenity.type"]
        Amenity = self.env["pms.amenity"]
        A1 = AmenityType.create(
            {
                "name": "TestAmenityType1",
                "pms_property_ids": [
                    (4, self.property1.id),
                    (4, self.property2.id),
                ],
            }
        )
        # ACT & ASSERT
        with self.assertRaises(ValidationError), self.cr.savepoint():
            Amenity.create(
                {
                    "name": "TestAmenity1",
                    "pms_amenity_type_id": A1.id,
                    "pms_property_ids": [
                        (
                            6,
                            0,
                            [self.property1.id, self.property2.id, self.property3.id],
                        )
                    ],
                }
            )

    def test_property_allowed(self):
        # Creation of a Amenity with Properties compatible with it Amenity Type
        # Check Properties of Amenity are in Properties of Amenity Type
        # +----------------------------------------+-----------------------------------+
        # |     Amenity Type (TestAmenityType1)    |      Amenity (TestAmenity1)       |
        # +----------------------------------------+-----------------------------------+
        # |    Property1 - Property2 - Property3   | Property1 - Property2 - Property3 |
        # +----------------------------------------+-----------------------------------+

        # ARRANGE
        self.create_common_scenario()
        AmenityType = self.env["pms.amenity.type"]
        Amenity = self.env["pms.amenity"]
        A1 = AmenityType.create(
            {
                "name": "TestAmenityType1",
                "pms_property_ids": [
                    (
                        6,
                        0,
                        [self.property1.id, self.property2.id, self.property3.id],
                    )
                ],
            }
        )
        # ACT
        TestAmenity = Amenity.create(
            {
                "name": "TestAmenity1",
                "pms_amenity_type_id": A1.id,
                "pms_property_ids": [
                    (
                        6,
                        0,
                        [self.property1.id, self.property2.id, self.property3.id],
                    )
                ],
            }
        )

        # ASSERT
        self.assertEqual(
            TestAmenity.pms_property_ids.ids,
            A1.pms_property_ids.ids,
            "Properties not allowed in amenity type",
        )

    def test_change_amenity_property(self):
        # Creation of a Amenity with Properties compatible with it Amenity Type
        # Delete a Property in Amenity Type, check Validation Error when do that
        # 1st scenario:
        # +----------------------------------------+-----------------------------------+
        # |     Amenity Type (TestAmenityType1)    |      Amenity (TestAmenity1)       |
        # +----------------------------------------+-----------------------------------+
        # |    Property1 - Property2 - Property3   | Property1 - Property2 - Property3 |
        # +----------------------------------------+-----------------------------------+
        # 2nd scenario(Error):
        # +----------------------------------------+-----------------------------------+
        # |     Amenity Type (TestAmenityType1)    |      Amenity (TestAmenity1)       |
        # +----------------------------------------+-----------------------------------+
        # |          Property1 - Property2         | Property1 - Property2 - Property3 |
        # +----------------------------------------+-----------------------------------+

        # ARRANGE
        self.create_common_scenario()
        AmenityType = self.env["pms.amenity.type"]
        Amenity = self.env["pms.amenity"]
        A1 = AmenityType.create(
            {
                "name": "TestAmenityType1",
                "pms_property_ids": [
                    (4, self.property1.id),
                    (4, self.property2.id),
                    (4, self.property3.id),
                ],
            }
        )
        # ACT
        Amenity.create(
            {
                "name": "TestAmenity1",
                "pms_amenity_type_id": A1.id,
                "pms_property_ids": [
                    (
                        6,
                        0,
                        [self.property1.id, self.property2.id, self.property3.id],
                    )
                ],
            }
        )
        # ASSERT
        with self.assertRaises(ValidationError):
            A1.pms_property_ids = [
                (
                    6,
                    0,
                    [self.property1.id, self.property2.id],
                )
            ]
            A1.flush()
