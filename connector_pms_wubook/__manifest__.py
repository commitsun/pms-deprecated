# Copyright 2018 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hotel Channel Connector Wubook',
    'version': '13.0.1.0.0',
    'author': "Alexandre Díaz <dev@redneboa.es>",
    'website': 'https://github.com/hootel/hootel',
    'category': 'hotel/connector',
    'summary': "Hotel Channel Connector Wubook",
    'description': "Hotel Channel Connector Wubook",
    'depends': [
        'connector_pms',
    ],
    'external_dependencies': {
        'python': ['pypi-xmlrpc']
    },
    'data': [
        'data/cron_jobs.xml',
        'data/sequences.xml',
        'data/records.xml',
        'views/inherited_channel_hotel_room_type_restriction_views.xml',
        'views/inherited_channel_connector_backend_views.xml',
        'views/inherited_channel_ota_info_views.xml',
        'views/inherit_res_company.xml',
        # 'security/wubook_security.xml',
        # 'views/res_config.xml'
    ],
    'test': [
    ],
    'installable': True,
    'license': 'AGPL-3',
}
