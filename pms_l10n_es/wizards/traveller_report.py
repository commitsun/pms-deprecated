from odoo import models, fields, api
import base64
from datetime import date
import datetime
from odoo.tools.translate import _
import unidecode


class TravellerReport(models.TransientModel):
    _name = 'traveller.report.wizard'

    sequence_num = fields.Char('Correlative number', default='New')
    txt_filename = fields.Char()
    txt_binary = fields.Binary()
    txt_message = fields.Char()

    def generate_file(self):
        # now = datetime.datetime.now()
        # previous_day = now-datetime.timezone(days=1)
        # range_time = [previous_day + timedelta(seconds=s) for s in range((now - previous_day).seconds + 1)]
        today = date.today()
        property = self.env["pms.property"].search([("id", "=", self.env.user.get_active_property_ids()[0])])
        lines = self.env['pms.checkin.partner'].search([
            ('state', '=', 'onboard') #,('arrival','=',today)
            ])
        if len(lines) == 0:
            return
        if property.police_number and property.name:
            content = "1|"+property.police_number+"|"+(property.name).upper()
            content += "|"
            content += datetime.datetime.now().strftime("%Y%m%d|%H%M")
            content += "|"+str(len(lines))
            checkin_count = 0
            for line in lines:
                if line.document_type == 'D':
                    content += "\n2|"+line.document_number.upper() +"||"
                else:
                    content += "\n2||"+line.document_number.upper() + "|"
                content += line.document_type+"|"
                content += (line.document_expedition_date).strftime("%Y%m%d") + "|"
                content += line.lastname.upper()+"|"
                if line.lastname2:
                    content += line.lastname2.upper()
                content += "|"+line.name.upper()+"|"
                if line.gender == "female":
                    content += "F|"
                else:
                    content += "M|"
                content += (line.birthdate_date).strftime("%Y%m%d") + "|"
                content += line.nationality_id.upper() + "|"
                content +=(line.arrival).strftime("%Y%m%d") + "|"
            print(content)
            print(self.sequence_num)
            return self.write({
                'txt_filename': property.police_number + '.' + self.sequence_num,
                'txt_message': _(
                    'Generated file. Download it and give it to the police.'),
                'txt_binary': base64.encodebytes(content.encode("iso-8859-1"))
                })
    @api.model
    def create(self, vals):
        if vals.get('sequence_num', 'New') == 'New':
            vals['sequence_num'] = self.env['ir.sequence'].next_by_code(
                'traveller.report.wizard') or 'New'
        result = super(TravellerReport, self).create(vals)
        return result
