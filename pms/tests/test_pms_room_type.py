from odoo.tests import common, tagged
class TestPmsRoomType(common.TransactionCase):

    def test_update_default_max_avail001(self):

        #ARRANGE
        room_type_set = self.env['pms.room.type'].search([('total_rooms_count', '>=', 2)])
        room_type_record = room_type_set[0]

        rooms_set = self.env['pms.room'].search([
            ('room_type_id', '=',room_type_record.id),
            ('active', '=',True)])

        #ACT
        rooms_set[0].active = False

        #ASSERT
        self.assertLessEqual(room_type_record.total_rooms_count \
            if room_type_record.default_max_avail == -1 else \
                room_type_record.default_max_avail , room_type_record.total_rooms_count,
        "The default maximum avail. is greater than the total room count for the room type")

    def test_update_default_max_avail002(self):

        #ARRANGE
        room_type_set = self.env['pms.room.type'].search([('total_rooms_count', '>=', 2)])
        room_type_record = room_type_set[0]

        self.env['pms.room'].create({
            'name': 'Test Room 1',
            'room_type_id': room_type_record.id
        }).create({
            'name': 'Test Room 2',
            'room_type_id': room_type_record.id
        })

        #ASSERT
        self.assertLessEqual(room_type_record.total_rooms_count \
            if room_type_record.default_max_avail == -1 else \
                room_type_record.default_max_avail , room_type_record.total_rooms_count,
        "The default maximum avail. is greater than the total room count for the room type")
