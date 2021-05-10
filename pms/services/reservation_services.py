from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class PmsReservationService(Component):
    _inherit = "base.rest.service"
    _name = "pms.service"
    _usage = "reservations"
    _collection = "pms.services"
    _description = """
        Reservation API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/"], "GET")],
        input_param=Datamodel("pms.reservation.search.param"),
        output_param=Datamodel("pms.reservation.short.info", is_list=True),
        auth="public",
    )
    def search(self, reservation_search_param):
        """
        Devuelve un listado de todas las reservas,
        admite parámetros de búsqueda 'id' y 'name'
        (ejs.: "/reservations", "/reservations?id=1&name=R/21003449")
        """
        domain = []
        if reservation_search_param.name:
            domain.append(("name", "like", reservation_search_param.name))
        if reservation_search_param.id:
            domain.append(("id", "=", reservation_search_param.id))
        res = []
        PmsReservationShortInfo = self.env.datamodels["pms.reservation.short.info"]
        for reservation in self.env["pms.reservation"].sudo().search(domain):
            res.append(
                PmsReservationShortInfo(
                    id=reservation.id,
                    partner=reservation.partner_id.name,
                    checkin=str(reservation.checkin),
                    checkout=str(reservation.checkout),
                    preferred_room_id=reservation.preferred_room_id.name
                    if reservation.preferred_room_id
                    else "",
                    room_type_id=reservation.room_type_id.name
                    if reservation.room_type_id
                    else "",
                    name=reservation.name,
                )
            )
        return res

    @restapi.method(
        [(["/<int:id>"], "GET")],
        output_param=Datamodel("pms.reservation.long.info"),
        auth="public",
    )
    def search_by_id(self, reservation_id):
        """
        Devuelve la reserva que se corresponde con el 'id' indicado
        (ej.: /reservations/34)
        """
        reservation = self.env["pms.reservation"].sudo().browse(reservation_id)
        if reservation:
            PmsReservationLongInfo = self.env.datamodels["pms.reservation.long.info"]
            return PmsReservationLongInfo(
                id=reservation.id,
                partner=reservation.partner_id.name,
                checkin=str(reservation.checkin),
                checkout=str(reservation.checkout),
                preferred_room_id=reservation.preferred_room_id.name
                if reservation.preferred_room_id
                else "",
                room_type_id=reservation.room_type_id.name
                if reservation.room_type_id
                else "",
                name=reservation.name,
                price=reservation.price_room_services_set,
                partner_requests=reservation.partner_requests
                if reservation.partner_requests
                else "",
            )

    @restapi.method(
        [(["/<int:id>/partner-requests"], "PATCH")],
        input_param=Datamodel("pms.reservation.patch.param"),
        output_param=Datamodel("pms.reservation.short.info"),
        auth="public",
    )
    def update_partner_requests(self, reservation_id, reservation_patch_params):
        """
        Actualiza el campo de peticiones de huéspedes para la reserva
         indicada con el id (ej.: /reservations/34)
        """
        reservation = self.env["pms.reservation"].sudo().browse(reservation_id)
        reservation.partner_requests = reservation_patch_params.partner_requests
        if reservation:
            PmsReservationShortInfo = self.env.datamodels["pms.reservation.short.info"]
            return PmsReservationShortInfo(
                id=reservation.id,
                partner=reservation.partner_id.name,
                checkin=str(reservation.checkin),
                checkout=str(reservation.checkout),
                preferred_room_id=reservation.preferred_room_id.name
                if reservation.preferred_room_id
                else "",
                room_type_id=reservation.room_type_id.name
                if reservation.room_type_id
                else "",
                name=reservation.name,
                price=reservation.price_room_services_set,
                partner_requests=reservation.partner_requests
                if reservation.partner_requests
                else "",
            )

    @restapi.method(
        [(["/<int:id>"], "DELETE")],
        output_param=Datamodel("pms.reservation.short.info"),
        auth="public",
    )
    def delete_reservation(self, reservation_id):
        """
        Borra la reserva indicada con el id (ej.: /reservations/34)
        """
        reservation = self.env["pms.reservation"].sudo().browse(reservation_id)
        if reservation:
            PmsReservationShortInfo = self.env.datamodels["pms.reservation.short.info"]
            result = PmsReservationShortInfo(
                id=reservation.id,
                partner=reservation.partner_id.name,
                checkin=str(reservation.checkin),
                checkout=str(reservation.checkout),
                preferred_room_id=reservation.preferred_room_id.name
                if reservation.preferred_room_id
                else "",
                room_type_id=reservation.room_type_id.name
                if reservation.room_type_id
                else "",
                name=reservation.name,
                price=reservation.price_room_services_set,
                partner_requests=reservation.partner_requests
                if reservation.partner_requests
                else "",
            )
            reservation.sudo().unlink()
            return result
