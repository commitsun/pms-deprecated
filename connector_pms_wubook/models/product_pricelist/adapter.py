# Copyright 2021 Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime

from odoo import _
from odoo.exceptions import ValidationError

from odoo.addons.component.core import Component
from odoo.addons.connector_pms.components.adapter import ChannelAdapterError


class ChannelWubookProductPricelistAdapter(Component):
    _name = "channel.wubook.product.pricelist.adapter"
    _inherit = "channel.wubook.adapter"

    _apply_on = "channel.wubook.product.pricelist"

    # CRUD
    # pylint: disable=W8106
    def create(self, values):
        # TODO: share common code from write method and availability plan
        # https://tdocs.wubook.net/wired/prices.html#add_vplan
        # https://tdocs.wubook.net/wired/prices.html#add_pricing_plan
        # https://tdocs.wubook.net/wired/prices.html#update_plan_prices
        # pricelist values
        if values.get("daily") == 0:
            raise ValidationError(_("Intensive plans not supported"))
        params = self._prepare_parameters(
            {k: values[k] for k in values if k in {"name", "daily"}},
            ["name"],
            ["daily"],
        )
        _id = self._exec("add_pricing_plan", *params)

        # pricelist item values
        items = values.get("items")
        if items:
            try:
                types = {x["type"] for x in items}
                if types == {"pricelist"}:
                    if len(items) != 1:
                        raise ValidationError(
                            _("Only one item of type 'pricelist' allowed")
                        )
                    params = self._prepare_parameters(
                        {
                            "name": "v%s" % values["name"],
                            "vpid": _id,
                            **{k: items[0][k] for k in {"variation_type", "variation"}},
                        },
                        ["name", "vpid", "variation_type", "variation"],
                    )
                    self._exec("add_vplan", *params)
                elif types == {"room"}:
                    prices = {}
                    dfrom = None
                    # TODO: allow gaps between dates grouping rooms
                    # and making multiple call to webservice
                    for i, room in enumerate(sorted(items, lambda x: x["date"])):
                        if not isinstance(room["date"], datetime.date):
                            raise ValidationError(
                                _("Date fields must be of type date, not %s")
                                % type(room["date"])
                            )
                        if not dfrom:
                            dfrom = room["date"]
                        else:
                            if dfrom + datetime.timedelta(days=i) != room["date"]:
                                raise ValidationError(_("There's gaps between dates"))
                        prices.setdefault(str(room["rid"]), []).append(room["price"])
                    params = self._prepare_parameters(
                        {
                            "id": _id,
                            "dfrom": dfrom.strftime(self._date_format),
                            "prices": prices,
                        },
                        ["id", "dfrom", "prices"],
                    )
                    self._exec("update_plan_prices", *params)
                else:
                    raise ValidationError(
                        _("Type %s not valid, only 'room' and 'pricelist' supported")
                        % types
                    )
            except ChannelAdapterError:
                self.delete(_id)
                raise

        return _id

    def read(self, _id):
        # https://tdocs.wubook.net/wired/prices.html#get_pricing_plans
        values = self.search_read([("id", "=", _id)])
        if not values:
            return False
        if len(values) != 1:
            raise ChannelAdapterError(_("Received more than one room %s") % (values,))
        return values[0]

    def search_read(self, domain):
        # self._check_supported_domain_format(domain)
        # https://tdocs.wubook.net/wired/prices.html#get_pricing_plans
        all_plans = self._exec("get_pricing_plans")
        real_pl_domain, common_pl_domain = self._extract_domain_clauses(
            domain, ["date", "rooms"]
        )
        base_plans = self._filter(all_plans, common_pl_domain)
        res = []
        for plan in base_plans:
            values = {x: plan[x] for x in ["id", "name", "daily"]}
            if values.get("daily") == 0:
                continue
            if "vpid" in plan:
                values["items"] = [
                    {
                        "type": "pricelist",
                        **{x: plan[x] for x in {"vpid", "variation", "variation_type"}},
                    }
                ]
            else:
                if real_pl_domain:
                    kw_params = self._domain_to_normalized_dict(real_pl_domain, "date")
                    kw_params["id"] = plan["id"]
                    params = self._prepare_parameters(
                        kw_params, ["id", "date_from", "date_to"], ["rooms"]
                    )
                    date_from = datetime.datetime.strptime(
                        kw_params["date_from"], self._date_format
                    ).date()
                    items_raw = self._exec("fetch_plan_prices", *params)
                    items = []
                    for rid, prices in items_raw.items():
                        for i, price in enumerate(prices):
                            items.append(
                                {
                                    "type": "room",
                                    "rid": int(rid),
                                    "date": date_from + datetime.timedelta(days=i),
                                    "price": price,
                                }
                            )
                    values["items"] = items
            res.append(values)
        return res

    def search(self, domain):
        # https://tdocs.wubook.net/wired/prices.html#get_pricing_plans
        values = self.search_read(domain)
        ids = [x[self._id] for x in values]
        return ids

    # pylint: disable=W8106
    def write(self, _id, values):
        # TODO: share common code from create method and availability plan
        # https://tdocs.wubook.net/wired/prices.html#update_plan_name
        # https://tdocs.wubook.net/wired/prices.html#mod_vplans
        # https://tdocs.wubook.net/wired/prices.html#update_plan_prices
        # pricelist values
        if "name" in values:
            params = self._prepare_parameters(
                {"id": _id, **{k: values[k] for k in values if k in {"name"}}},
                ["id", "name"],
            )
            self._exec("update_plan_name", *params)

        # pricelist item values
        items = values.get("items")
        if items:
            types = {x["type"] for x in items}
            if types == {"pricelist"}:
                if len(items) != 1:
                    raise ValidationError(
                        _("Only one item of type 'pricelist' allowed")
                    )
                params = self._prepare_parameters(
                    {
                        "plans": [
                            {
                                "pid": _id,
                                **{
                                    k: items[0][k]
                                    for k in {"variation_type", "variation"}
                                },
                            }
                        ]
                    },
                    ["plans"],
                )
                self._exec("mod_vplans", *params)
            elif types == {"room"}:
                prices = {}
                dfrom = None
                for i, room in enumerate(sorted(items, key=lambda x: x["date"])):
                    if not isinstance(room["date"], datetime.date):
                        raise ValidationError(
                            _("Date fields must be of type date, not %s")
                            % type(room["date"])
                        )
                    if not dfrom:
                        dfrom = room["date"]
                    else:
                        if dfrom + datetime.timedelta(days=i) != room["date"]:
                            raise ValidationError(_("There's gaps between dates"))
                    prices.setdefault(str(room["rid"]), []).append(room["price"])
                params = self._prepare_parameters(
                    {
                        "id": _id,
                        "dfrom": dfrom.strftime(self._date_format),
                        "prices": prices,
                    },
                    ["id", "dfrom", "prices"],
                )
                self._exec("update_plan_prices", *params)
            else:
                raise ValidationError(
                    _("Type %s not valid, only 'room' and 'pricelist' supported")
                    % types
                )

    def delete(self, _id, cascade=False):
        # TODO: optimize
        # https://tdocs.wubook.net/wired/prices.html#del_plan
        if cascade:
            res = self.search_read([])
            for pl in res:
                if pl.get("items", {}).get("vpid") == _id:
                    self.delete(pl["id"], cascade=False)
        self._exec("del_plan", _id)
