from odoo.tests import common, tagged
@tagged('-at_install', 'post_install')

class TestAmenities(common.TransactionCase):

    def setUp(self):
        super(TestAmenities, self).setUp()
        print("before any test case")

    def tearDown(self):
        super(TestAmenities, self).tearDown()
        print("after any test case")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("before all test cases")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("after all test cases")

    def test_create_amenity_001(self):
        #ARRANGE
        amenity_type =  self.ref('pms.pms_amenity_type_0')
        property_id =  self.ref('pms.demo_pms_property')
        expected = self.env['pms.amenity'].search_count([('room_amenity_type_id', '=', amenity_type)])
        expected += 1
        amenity_vals = {
            'name': 'soap',
            'room_amenity_type_id': amenity_type,
            'pms_property_ids': [property_id]
        }
        #ACT
        operation = self.env['pms.amenity'].create(amenity_vals)
        actual = self.env['pms.amenity'].search_count(
            [('room_amenity_type_id', '=', amenity_type)]
        )
        #ASSERT
        self.assertEqual(actual, expected, "Amenity not created")

    def test_create_amenity_002(self):
        #ARRANGE
        amenity_type =  self.ref('pms.pms_amenity_type_0')
        property_id =  self.ref('pms.demo_pms_property')
        expected = self.env['pms.amenity'].search_count([('room_amenity_type_id', '=', amenity_type)])
        expected += 1
        amenity_vals = {
            'name': '', # <--- Empty name
            'room_amenity_type_id': amenity_type,
            'pms_property_ids': [property_id]
        }
        #ACT
        operation = self.env['pms.amenity'].create(amenity_vals)
        actual = self.env['pms.amenity'].search_count(
            [('room_amenity_type_id', '=', amenity_type)]
        )
        #ASSERT
        self.assertNotEqual(actual, expected, "Amenity created")

    def test_create_amenity_003(self):
        #ARRANGE
        amenity_type =  self.ref('pms.pms_amenity_type_0')
        property_id =  self.ref('pms.demo_pms_property')
        expected = self.env['pms.amenity'].search_count([('room_amenity_type_id', '=', amenity_type)])
        expected += 1
        amenity_vals = {
            'name': 'soap',
            'room_amenity_type_id': None, # <--- None
            'pms_property_ids': [property_id]
        }
        #ACT
        operation = self.env['pms.amenity'].create(amenity_vals)
        actual = self.env['pms.amenity'].search_count(
            [('room_amenity_type_id', '=', amenity_type)]
        )
        #ASSERT
        self.assertEqual(actual, expected, "Amenity not created")



