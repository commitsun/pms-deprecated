# © 2020  Dario Lodeiros
# © 2020  Eric Antones
from odoo import _, api, field, models
from odoo.exceptions import UserError


class BaseModel(models.AbstractModel):
    _inherit = "base"
    _check_pms_properties_auto = False
    """On write and create, call ``_check_pms_properties_auto`` to ensure properties
    consistency on the relational fields having ``check_pms_properties=True``
    as attribute.
    """

    @api.model_create_multi
    @api.returns("self", lambda value: value.id)
    def create(self, vals_list):
        records = super(BaseModel, self).create(vals_list)
        if self._check_pms_properties_auto:
            records._check_pms_properties()

    def write(self, vals):
        res = super(BaseModel, self).write(vals)
        check_pms_properties = False
        for fname in vals:
            if fname == "property_id" or (
                field.relational and field.check_pms_properties
            ):
                check_pms_properties = True
        if res and check_pms_properties and self._check_pms_properties_auto:
            self._check_pms_properties()
        return res

    def _check_pms_properties(self, fnames=None):
        """Check the properties of the values of the given field names.

        :param list fnames: names of relational fields to check
        :raises UserError: if the `pms_properties` of the value of any field is not
            in `[False, self.property_id]` (or `self` if
            :class:`~odoo.addons.base.models.pms_property`).

        For :class:`~odoo.addons.base.models.res_users` relational fields,
        verifies record company is in `company_ids` fields.

        User with main pms property A, having access to pms property A and B, could be
        assigned or linked to records in property B.
        """
        if fnames is None:
            fnames = self._fields

        regular_fields = []
        for name in fnames:
            field = self._fields[name]
            if (
                field.relational
                and field.check_pms_properties
                and (
                    "pms_property_id" in self.env[field.comodel_name]
                    or "pms_property_ids" in self.env[field.comodel_name]
                )
            ):
                regular_fields.append(name)

        if not regular_fields:
            return

        inconsistencies = []
        for record in self:
            pms_properties = False
            if record.name == "pms.property":
                pms_properties = record
            if "pms_property_id" in record:
                pms_properties = record.pms_property_id
            if "pms_property_ids" in record:
                pms_properties = record.pms_property_ids
            # Check verifies that all
            # records linked via relation fields are compatible
            # with the properties of the origin document,
            for name in regular_fields:
                co_pms_properties = False
                corecord = record.sudo()[name]
                if "pms_property_id" in corecord:
                    co_pms_properties = corecord.pms_property_id
                if "pms_property_ids" in corecord:
                    co_pms_properties = corecord.pms_property_ids
                if (
                    pms_properties
                    and co_pms_properties
                    and not pms_properties & co_pms_properties
                ):
                    inconsistencies.append((record, name, corecord))

        if inconsistencies:
            lines = [_("Incompatible properties on records:")]
            property_msg = _(
                """- Record is properties %(pms_properties)r and %(field)r
                (%(fname)s: %(values)s) belongs to another properties."""
            )
            record_msg = _(
                """- %(record)r belongs to properties %(pms_properties)r and
                %(field)r (%(fname)s: %(values)s) belongs to another properties."""
            )
            for record, name, corecords in inconsistencies[:5]:
                if record._name == "pms.property":
                    msg, pms_properties = property_msg, record
                else:
                    msg, pms_properties = (
                        record_msg,
                        record.property_id.name
                        if "pms_property_id" in record
                        else ", ".join(repr(p.name) for p in record.property_ids),
                    )
                field = self.env["ir.model.fields"]._get(self._name, name)
                lines.append(
                    msg
                    % {
                        "record": record.display_name,
                        "pms_properties": pms_properties,
                        "field": field.field_description,
                        "fname": field.name,
                        "values": ", ".join(
                            repr(rec.display_name) for rec in corecords
                        ),
                    }
                )
            raise UserError("\n".join(lines))
