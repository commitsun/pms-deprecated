from odoo.exceptions import ValidationError
from odoo.tests import common

# TODO: Eliminar el common y basarse (pegar repaso al resto de los tests y eliminar common)


class TestPmsAmenity(common.SavepointCase):
    def create_common_scenario(self):
        # create company and properties
        # TODO:  Scenario digest
        self.company1 = self.env["res.company"].create(
            {
                "name": "Pms_Company_Test",
            }
        )
        self.property1 = self.env["pms.property"].create(
            {
                "name": "Pms_property_test1",
                "company_id": self.company1.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
            }
        )
        self.property2 = self.env["pms.property"].create(
            {
                "name": "Pms_property_test2",
                "company_id": self.company1.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
            }
        )

        self.property3 = self.env["pms.property"].create(
            {
                "name": "Pms_property_test3",
                "company_id": self.company1.id,
                "default_pricelist_id": self.env.ref("product.list0").id,
            }
        )

    def test_property_not_allowed(self):
        # TODO: Creación de una amenity con compañías incompatibles con el tipo
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

    # TODO Test1: Test caso valido del de arriba

    # TODO Test2: Test modificación de properties de correcto a incorrecto
