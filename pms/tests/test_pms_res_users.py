from odoo.exceptions import ValidationError
from odoo.tests import common


class TestPmsResUser(common.TransactionCase):
    def create_common_scenario(self):
        # create a room type availability
        self.room_type_availability = self.env[
            "pms.room.type.availability.plan"
        ].create({"name": "Availability plan 1"})

        # create a company and properties
        self.company_A = self.env["res.company"].create(
            {
                "name": "Pms_Company1",
            }
        )
        self.company_B = self.env["res.company"].create(
            {
                "name": "Pms_Company2",
            }
        )
        self.property_A1 = self.env["pms.property"].create(
            {
                "name": "Pms_property",
                "company_id": self.company_A.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
                "default_availability_plan_id": self.room_type_availability.id,
            }
        )
        self.property_A2 = self.env["pms.property"].create(
            {
                "name": "Pms_property2",
                "company_id": self.company_A.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
                "default_availability_plan_id": self.room_type_availability.id,
            }
        )
        self.property_B1 = self.env["pms.property"].create(
            {
                "name": "Pms_propertyB1",
                "company_id": self.company_B.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
                "default_availability_plan_id": self.room_type_availability.id,
            }
        )

    def test_property_not_allowed(self):
        """
        Property not allowed, it belongs to another company

        Company_A ---> Property_A1, Property_A2
        Company_B ---> Property_B1

        """
        # ARRANGE
        name = "test user"
        login = "test_user"
        self.create_common_scenario()
        Users = self.env["res.users"]
        # ACT & ASSERT
        with self.assertRaises(ValidationError), self.cr.savepoint():
            Users.create(
                {
                    "name": name,
                    "login": login,
                    "company_ids": [(4, self.company_A.id)],
                    "company_id": self.company_A.id,
                    "pms_property_ids": [(4, self.property_A1.id)],
                    "pms_property_id": self.property_B1.id,
                }
            )

    def test_check_allowed_property_ids(self):
        # ARRANGE
        name = "test user2"
        login = "test_user2"
        self.create_common_scenario()
        Users = self.env["res.users"]
        # ACT & ASSERT
        with self.assertRaises(ValidationError), self.cr.savepoint():
            Users.create(
                {
                    "name": name,
                    "login": login,
                    "company_ids": [(4, self.company_A.id)],
                    "company_id": self.company_A.id,
                    "pms_property_ids": [
                        (4, self.property_A1.id),
                        (4, self.property_B1.id),
                    ],
                    "pms_property_id": self.property_A1.id,
                }
            )
