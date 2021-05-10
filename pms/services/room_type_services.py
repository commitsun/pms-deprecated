from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class PmsRoomTypeServices(Component):
    _inherit = "base.rest.service"
    _name = "pms.room.type.service"
    _usage = "room-types"
    _collection = "pms.services"
    _description = """
        Room type API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/"], "GET")],
        input_param=Datamodel("pms.room.type.short.info"),
        output_param=Datamodel("pms.room.type.short.info", is_list=True),
        auth="public",
    )
    def search(self, room_type_search_param):
        """
        Devuelve un listado de todos los tipos de habitación,
        admite parámetros de búsqueda 'id' y 'name'
        (ejs.: "/room-types", "/room-types?id=1&name=R/21003449")
        """
        domain = []
        if room_type_search_param.name:
            domain.append(("name", "like", room_type_search_param.name))
        if room_type_search_param.id:
            domain.append(("id", "=", room_type_search_param.id))
        res = []
        PmsReservationShortInfo = self.env.datamodels["pms.room.type.short.info"]
        for room_type in self.env["pms.room.type"].sudo().search(domain):
            res.append(
                PmsReservationShortInfo(
                    id=room_type.id,
                    name=room_type.name,
                )
            )
        return res
