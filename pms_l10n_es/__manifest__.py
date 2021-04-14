# Copyright 2020 CommitSun (<http://www.commitsun.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "PMS Spanish Adaptation",
    "version": "14.0.1.0.0",
    "author": "CommitSun, " "Odoo Community Association (OCA), " "Jose Luis Algara",
    "license": "AGPL-3",
    "application": True,
    "category": "Localization",
    "website": "https://github.com/OCA/pms",
    "depends": [
        "pms",
        "partner_firstname",
        "partner_second_lastname",
        "partner_contact_gender",
        "partner_contact_birthdate",
    ],
    "data": [
        "data/code.ine.csv",
        "views/pms_checkin_partner_views.xml",
        "views/res_partner_views.xml",
        "views/code_ine.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
