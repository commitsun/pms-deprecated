# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mandatory fiels adaptation to spanish law",
    "version": "14.0.1.0.0",
    "author": "CommitSun, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "category": "Extra Tools",
    # "website": "https://github.com/OCA/partner-contact",
    "depends": [
        "pms",
        "partner_firstname",
        # "partner_lastname",
        # "partner_contact_gender",
        # "partner_vat_unique"
        # "parner_contact_birthdate"
    ],
    "post_init_hook": "post_init_hook",
    "data": [
        # "views/res_partner.xml",
    ],
    "auto_install": False,
    "installable": True,
}
