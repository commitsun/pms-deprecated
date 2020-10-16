from odoo.tests import common, tagged
class TestPmsRoomType(common.TransactionCase):

    def test_update_default_max_avail(self):

        #ARRANGE
        record_room_type = self.browse_ref('pms.pms_room_type_2')
        rooms = self.env['pms.room'].search([('room_type_id', '=',record_room_type.id)])
        record_room_type.default_max_avail = record_room_type.total_rooms_count

        #ACT
        if rooms:
            rooms[0].active = False

        #ASSERT
        self.assertLessEqual(record_room_type.default_max_avail, record_room_type.total_rooms_count,
        "The default maximum availability is greater than the total room count for a type")
