# Copyright 2019-2021 Jose Luis Algara (Alda hotels) <osotranquilo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


def get_years():
    """Return a year list, to select in year field."""
    year_list = []
    for i in range(2018, 2036):
        year_list.append((str(i), str(i)))
    return year_list


class Budget(models.Model):
    """Establish and save the budget for DataBI control by revenue"""

    _name = "pms.budget"

    # fecha Primer día del mes
    month = fields.Selection(
        string="Month",
        selection=[
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        required=True,
    )
    year = fields.Selection(get_years(), string="Year", required=True)
    room_nights = fields.Float("Room Nights", required=True, digits=(6, 2))
    # Número de Room Nights
    room_revenue = fields.Float("Room Revenue", required=True, digits=(6, 2))
    # Ingresos por Reservas
    estancias = fields.Integer("Number of Stays")  # Número de Estancias
    # ID_Tarifa numérico Código de la Tarifa
    # ID_Canal numérico Código del Canal
    # ID_Pais numérico Código del País
    # ID_Regimen numérico Cóigo del Régimen
    # ID_Tipo_Habitacion numérico Código del Tipo de Habitación
    # iD_Segmento numérico Código del Segmento
    # ID_Cliente numérico Código del Cliente
    # Pension_Revenue numérico con dos decimales Ingresos por Pensión
    pms_property_id = fields.Many2one(
        "pms.property",
        required=True,
        ondelete="restrict",
        default=lambda self: self.env.user.get_active_property_ids()[0],
    )
