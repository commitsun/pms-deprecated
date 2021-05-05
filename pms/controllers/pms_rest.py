from odoo.addons.base_rest.controllers import main


class BaseRestDemoPublicApiController(main.RestController):
    _root_path = "/api/"
    _collection_name = "pms.services"
    _default_auth = "public"
