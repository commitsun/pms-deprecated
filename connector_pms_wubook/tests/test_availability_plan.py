# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
import logging

from odoo.tests.common import tagged

from . import common, server

_logger = logging.getLogger(__name__)


# @tagged("test_debug")
class TestAV(common.TestWubookConnector):
    def test_av(self):
        import json

        with open("wubook_auth.json", "r") as f:
            backend_values = json.load(f)

        property1 = self.ref("pms.main_pms_property")
        backend_values.update(
            {
                "name": "Test backend",
                "pms_property_id": property1.id,
                "user_id": self.user1(property1).id,
                "model_id": self.ref(
                    "connector_pms_wubook.model_channel_wubook_backend"
                ),
            }
        )
        backend = self.env["channel.wubook.backend"].create(backend_values)

        # -----------------------------------

        # self.env["channel.wubook.pms.room.type.class"].import_data(backend)
        # self.env["channel.wubook.pms.room.type"].import_data(backend)

        # self.env["channel.wubook.pms.room.type"].import_data(backend,
        #     datetime.date(2021,2,14), datetime.date(2021,2,15), None, None)

        with backend.work_on("channel.wubook.pms.availability.plan") as work:
            adapter = work.component(usage="backend.adapter")

        res = adapter.search_read([])
        print("vvvvvvvvvvvvvvv", res)

        # res = adapter.create({'name': 'test8'})

        # res = adapter.search_read([('id', '=', 85448)])
        # res = adapter.search_read([('id', 'in', (85448,85447,))])
        # res = adapter.search_read([])
        # for r in res:
        #     adapter.delete(r['id'])
        #     print(r)

        # res = adapter.search_read([
        #     # ('id', '=', 85448),
        #     ('dfrom', '=', datetime.date(2021, 3, 25)),
        #     ('dto', '=', datetime.date(2021, 3, 27))
        # ])
        # print("vvvvvvvvvvvvvvv", res)

        # res = adapter.create({
        #     'name': 'test119',
        #     'items': [
        #         {
        #             'id_room': 478489,
        #             'date': datetime.date(2021, 3, 25),
        #             'closed': 1,
        #             'max_stay': 5,
        #             'min_stay_arrival': 7,
        #             'avail': 9,
        #         }
        #     ]
        # })
        # print(res)
        # res = adapter.search_read([
        #     # ('id', '=', 85448),
        #     ('name', '=', 'test119'),
        #     ('dfrom', '=', datetime.date(2021, 3, 25)),
        #     ('dto', '=', datetime.date(2021, 3, 27))
        # ])
        # print("vvvvvvvvvvvvvvv", res)

        res = adapter.create(
            {
                "name": "test99K",
                "items": [
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 2, 24),
                        "closed": 1,
                        "max_stay": 8,
                        "min_stay_arrival": 9,
                    },
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 2, 26),
                        "closed": 1,
                        "max_stay": 18,
                        "min_stay_arrival": 89,
                    },
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 2, 28),
                        "closed": 1,
                        "max_stay": 178,
                        "min_stay_arrival": 879,
                    },
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 3, 28),
                        "closed": 0,
                        "max_stay": 23,
                        "min_stay_arrival": 9,
                    },
                ],
            }
        )

        print("XXXXXXXXXXXX", res)

        return
        res = adapter.write(
            86122,
            {
                "name": "test101-renamed2",
                "items": [
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 3, 24),
                        "closed": 1,
                        "max_stay": 8,
                        "min_stay_arrival": 9,
                        "no_ota": 1,
                        "avail": 11,
                    },
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 3, 26),
                        "closed": 1,
                        "max_stay": 18,
                        "min_stay_arrival": 89,
                        "avail": 13,
                    },
                    {
                        "id_room": 477968,
                        "date": datetime.date(2021, 3, 28),
                        "closed": 1,
                        "max_stay": 178,
                        "min_stay_arrival": 879,
                    },
                ],
            },
        )

        res = adapter.search_read(
            [
                ("id", "=", 86122),
                # ('name', '=', 'test119'),
                ("dfrom", "=", datetime.date(2021, 3, 24)),
                ("dto", "=", datetime.date(2021, 3, 28)),
            ]
        )
        print("vvvvvvvvvvvvvvv", res)

        return

        # ---------------------------------------------

        # with backend.work_on("channel.wubook.product.pricelist") as work:
        #     binding_model = work.model
        #
        # binding_model.import_batch(backend, domain=[('name', '=', 'vtest68')])
        #
        # binding_model.import_batch(backend, domain=[('name', '=', 'vtest68')])
        #
        # av = self.env["channel.wubook.product.pricelist"].search([])
        # for i in av:
        #     print(i)
        #
        # a = 1
        #
        # return

        # ---------------------------------------------

        # parent = self.env["channel.wubook.product.pricelist"].create({
        #     'name': 'child',
        #     'backend_id': backend.id,
        # })
        # print("222222222222222 --------------", parent, parent.name)
        #
        # parent.write({
        #     'name': 'pepe',
        #     'item_ids': [(0, 0, {
        #         'applied_on': '3_global',
        #         'compute_price': 'formula',
        #         # 'base': 'pricelist',
        #         # 'base_pricelist_id': parent.odoo_id.id,
        #         # 'price_discount': 69,
        #         # 'pricelist_id': child.odoo_id.id,
        #     })]
        # })
        # print("333333333333333333 --------------------", parent, parent.name,
        #       parent.item_ids, parent.item_ids.compute_price,
        #       parent.item_ids.pricelist_id.name)
        #
        # # child.write({
        # #     'name': 'uu',
        # # })
        # parent.write({
        #     'name': 'uu',
        #     'sequence': 66,
        #     'item_ids': [
        #         (1, parent.item_ids.id, {
        #             'applied_on': '3_global',
        #             'compute_price': 'fixed',
        #             # 'base': 'pricelist',
        #             # 'base_pricelist_id': parent.odoo_id.id,
        #             # 'price_discount': 88,
        #             # 'pricelist_id': child.odoo_id.id,
        #         })]
        # })
        # print("4444444444444444 --------------", parent, parent.name, parent.item_ids,
        #       parent.item_ids.compute_price,
        #       parent.item_ids.pricelist_id.name, parent.sequence)
        #
        # return

        # with backend.work_on("channel.wubook.pms.room.type") as work:
        #     adapter = work.component(usage="backend.adapter")
        #     print(adapter.search_read([('shortname', '=', 'H217')]))

        with backend.work_on("channel.wubook.product.pricelist") as work:
            adapter = work.component(usage="backend.adapter")
            print("----------------__", adapter)
            # res = adapter.create({'name': 'TEST55'})
            res = adapter.search_read([])
            print("**", res)
            # res = adapter.search_read([('id', '=', 178429)])
            # res = adapter.search_read([('id', 'in', [178429, 178424,178428,])])
            # res = adapter.search_read([('name', '=', 'TEST55')])
            # res = adapter.search_read([
            #     #('id', 'in', [178429, 178424, 178428]),
            #     #('dfrom', '=', datetime.date(2021, 2, 1)),
            #     #('dto', '=', datetime.date(2021, 2, 2)),
            #     #('rooms', 'in', [478457, 478459]),
            #     # ('av', '=', 6565)
            #     ('vpid', '=', 178428)
            # ])
            # res = adapter.read(178428)
            # print("******", res)

            # res = adapter.write(178538, {
            #     'name': 'vT445',
            #     'items': [{
            #         'type': 'pricelist',
            #         'variation': 11,
            #         'variation_type': 2
            #     }]
            # })
            # print("************", res)

            # test de rooms
            res = adapter.write(
                178538,
                {
                    "name": "vT445",
                    "items": [
                        {"type": "pricelist", "variation": 11, "variation_type": 2}
                    ],
                },
            )
            print("************", res)

            res = adapter.search_read([("id", "=", 178538)])
            print("******", res)

            # res = adapter.create({
            #     'name': 'T445',
            #     'items': [{
            #         'type': 'pricelist',
            #         'variation': 10,
            #         'variation_type': -1,
            #     }]
            # })
            # print("******", res)

            # res = adapter.search_read([])
            # print("**", res)
            #
            # res = adapter.write(178428, {
            #     'variation': 66,
            #     'variation_type': -1
            # })
            # print("**", res)
            #
            #
            # res = adapter.search_read([])
            # print("**", res)
            # res = adapter.delete(177581)
            # print(res)
            # res = adapter.search_read([('name', '=', 'TEST55'), ('vpid', '!=', False)])
            # print("**", res)
            # res = adapter.write(178427, {'name':'test11'})
            # print("**", res)
            # res = adapter.write(178429, {
            #     'rack': {str(477968): [63, 64, 65, 66, 67, 68, 69]}
            # })
            # res = adapter.write(178429, {
            #     'rack': {str(477968): [63, 64, 65, 66, 67, 68, 69]}
            # })
            # res = adapter.write(178427, {'name':'test11'})
            # print("**", res)

            # res = adapter.search_read([])
            # print("**", res)

        # with backend.work_on("channel.wubook.product.pricelist.item") as work:
        #     adapter = work.component(usage="backend.adapter")
        #
        #     # res = adapter.search_read([])
        #
        #     dfrom = datetime.datetime(2021, 1, 1)
        #     dto = datetime.datetime(2021, 2, 8)
        #     res = adapter.search_read([
        #         ('vpid', '=', 178429), # real
        #         #('vpid', '=', 178428), # virtual
        #         ('dfrom', '=', dfrom),
        #         ('dto', '=', dto),
        #         ('rooms', 'in', [478457, 478459]),
        #         #('av', '=', 6565)
        #     ])
        #     print("*", res)

        return

        r1 = self.env["pms.room.type"].create(
            {
                "name": "Room type r1",
                "list_price": 1.0,
                "default_code": "H217",
                "pms_property_ids": [(6, 0, [self.ref("pms.main_pms_property")])],
                "company_id": False,
            }
        )

        with backend.work_on("channel.wubook.pms.room.type") as work:
            # adapter = work.component(usage="backend.adapter")
            # external_data = adapter.search_read([('shortname', '=', 'H217')])
            # print(external_data)
            #
            # mapper = work.component(usage="import.mapper")
            # map_vals = mapper.map_record(external_data[0])
            # vals = map_vals.values(for_create=True, fields=['shortname', 'name'])
            # print(vals)

            mapper = work.component(usage="export.mapper")
            t = work.model.create(
                {
                    "odoo_id": r1.id,
                    "backend_id": backend.id,
                }
            )
            map_vals = mapper.map_record(t)
            vals = map_vals.values(for_create=True)  # , fields=['shortname', 'name'])
            # print(vals)


# class TestWubookConnectorProductPricelistImport(common.TestWubookConnector):
#     # non-existing
#     @mock.patch.object(xmlrpc.client, "Server")
#     def test_import_non_existing_case01(self, mock_xmlrpc_client_server):
#         """
#         PRE:    - room type r1 does not exist
#         ACT:    - import r1 from property p1
#         POST:   - room type r1 imported
#                 - r1 has the values from the backend
#         """
#         # mock object
#         mock_server = common.WubookMockServer()
#         mock_xmlrpc_client_server.return_value = mock_server.get_mock()
#
#         # ARRANGE
#         p1 = self.browse_ref("pms.main_pms_property")
#         backend = self.env["channel.wubook.backend"].create(
#             {
#                 "name": "Test backend",
#                 "pms_property_id": p1.id,
#                 "model_id": self.ref(
#                     "connector_pms_wubook.model_channel_wubook_backend"
#                 ),
#                 "username": "X",
#                 "password": "X",
#                 "property_code": "X",
#                 "pkey": "X",
#             }
#         )
#
#         with backend.work_on("channel.wubook.pms.room.type") as work:
#             adapter = work.component(usage="backend.adapter")
#
#         r1w_values = {
#             "name": "Room type r1",
#             "shortname": "c1",
#             "price": 1.0,
#             "availability": 2,
#             "board": "ai",
#             "occupancy": 6,
#             "woodoo": 0,
#         }
#         r1w_id = adapter.create(r1w_values)
#
#         # ACT
#         backend.import_room_types()
#
#         # ASSERT
#         with backend.work_on("channel.wubook.pms.room.type") as work:
#             binder = work.component(usage="binder")
#         r1 = binder.to_internal(r1w_id, unwrap=True)
#
#         mapped_fields = [
#             ("name", "name"),
#             ("shortname", "default_code"),
#             ("price", "list_price"),
#         ]
#         odoo_values = [getattr(r1, x) for _, x in mapped_fields] + [r1.pms_property_ids]
#         wubook_values = [r1w_values.get(x) for x, _ in mapped_fields] + [
#             backend.pms_property_id
#         ]
#
#         self.assertListEqual(
#             odoo_values,
#             wubook_values,
#             "The room type data on Odoo does not match the data on Wubook",
#         )
