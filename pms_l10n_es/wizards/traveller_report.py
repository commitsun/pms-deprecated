import base64
import datetime
from datetime import date

import os
import requests
from bs4 import BeautifulSoup as bs

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class TravellerReport(models.TransientModel):
    _name = "traveller.report.wizard"
    _description = "Traveller Report"

    txt_filename = fields.Text()
    txt_binary = fields.Binary(
        string="File Download"
    )
    txt_message = fields.Char(
        string="File Preview"
    )

    def generate_file(self):

        # get the active property
        pms_property = self.env["pms.property"].search(
            [("id", "=", self.env.user.get_active_property_ids()[0])]
        )

        # build content
        content = self.generate_checkin_list(pms_property.id)

        # file creation
        txt_binary = self.env["traveller.report.wizard"].create(
            {
                "txt_filename": pms_property.institution_property_id
                + ".999",
                "txt_binary": base64.b64encode(str.encode(content)),
                "txt_message": content,
            }
        )
        return {
            "name": _("Preview & Send File"),
            "res_id": txt_binary.id,
            "res_model": "traveller.report.wizard",
            "target": "new",
            "type": "ir.actions.act_window",
            "view_id": self.env.ref("pms_l10n_es.traveller_report_wizard").id,
            "view_mode": "form",
            "view_type": "form",
        }

    def generate_checkin_list(self, property_id):

        # check if there's guests info pending to send
        if (
            self.env["pms.checkin.partner"].search_count(
                [
                    ("state", "=", "onboard"),
                    ("arrival", ">=", str(date.today()) + " 0:00:00"),
                    ("arrival", "<=", str(date.today()) + " 23:59:59"),
                ]
            )
            == 0
        ):
            raise ValidationError(_("There's no guests info to send"))
        else:

            # get the active property
            pms_property = self.env["pms.property"].search([("id", "=", property_id)])

            # check if the GC configuration info is properly set
            if not (
                pms_property.name
                and pms_property.institution_property_id
                and pms_property.institution_user
                and pms_property.institution_password
            ):
                raise ValidationError(
                    _("Check the GC configuration to send the guests info")
                )
            else:
                # get checkin partners info to send
                lines = self.env["pms.checkin.partner"].search(
                    [
                        ("state", "=", "onboard"),
                        ("arrival", ">=", str(date.today()) + " 0:00:00"),
                        ("arrival", "<=", str(date.today()) + " 23:59:59"),
                    ]
                )

                # build the property info record
                # 1 | property id | property name | date | nº of checkin partners

                content = (
                    "1|"
                    + pms_property.institution_property_id.upper()
                    + "|"
                    + pms_property.name.upper()
                    + "|"
                    + datetime.datetime.now().strftime("%Y%m%d|%H%M")
                    + "|"
                    + str(len(lines))
                    + "\n"
                )

            # build each checkin partner line's record
            # 2|DNI nº|Doc.number|doc.type|exp.date|lastname|lastname2|name|...
            # ...gender|birthdate|nation.|checkin

            for line in lines:
                content += "2"
                # [P|N|..]
                if line.document_type != "D":
                    content += "||" + line.document_number.upper() + "|"
                else:
                    content += "|" + line.document_number.upper() + "||"
                content += line.document_type + "|"
                content += line.document_expedition_date.strftime("%Y%m%d") + "|"
                content += line.lastname.upper() + "|"
                if line.lastname2:
                    content += line.lastname2.upper()
                content += "|" + line.firstname.upper() + "|"
                if line.gender == "female":
                    content += "F|"
                else:
                    content += "M|"
                content += line.birthdate_date.strftime("%Y%m%d") + "|"
                content += line.nationality_id.name.upper() + "|"
                content += line.arrival.strftime("%Y%m%d") + "\n"

            return content

    def send_file_gc(self, pms_property=False):
        url = "https://hospederias.guardiacivil.es/"
        login_route = "/hospederias/login.do"
        upload_file_route = "/hospederias/cargaFichero.do"
        called_from_user = False
        if not pms_property:
            called_from_user = True
            # get the active property
            pms_property = self.env["pms.property"].search(
                [("id", "=", self.env.user.get_active_property_ids()[0])]
            )

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 "
                          "Build/MRA58N) AppleWebKit/537.36 (KHTML, like "
                          "Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
        }
        s = requests.session()
        login_payload = {
            "usuario": pms_property.institution_user,
            "pswd": pms_property.institution_password,
        }
        s.post(
            url + login_route,
            headers=headers,
            data=login_payload,
            verify=get_module_resource("pms_l10n_es", "static", "cert.pem"),
            )

        pwd = get_module_resource("pms_l10n_es", "wizards", "")
        checkin_list_file = open(pwd + pms_property.institution_user + ".999", "w+")
        checkin_list_file.write(self.generate_checkin_list(pms_property.id))
        checkin_list_file.close()
        files = {"fichero": open(pwd + pms_property.institution_user + ".999", "rb")}

        response_file_sent = s.post(
            url + upload_file_route,
            data={"autoSeq": "on"},
            files=files,
            verify=get_module_resource("pms_l10n_es", "static", "cert.pem"),
            )
        os.remove(pwd + pms_property.institution_user + ".999")
        s.close()

        soup = bs(response_file_sent.text, "html.parser")
        errors = soup.select("#errores > tbody > tr > td > a")
        if errors:
            raise ValidationError(errors[2].text)
        else:
            if called_from_user:
                message = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Sent succesfully!'),
                        'message': _('Successful file sending'),
                        'sticky': False,
                    }
                }
                return message

    @api.model
    def send_file_gc_async(self):
        for prop in self.env["pms.property"].search([]):
            self.with_delay().send_file_gc(prop)
