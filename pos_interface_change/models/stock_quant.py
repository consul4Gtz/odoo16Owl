# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from odoo.tools import float_is_zero
import json
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def create(self, vals):
        res = super(StockQuant, self).create(vals)

        notifications = []
        for rec in res:
            prod_data = rec.product_id.read(
                ['id', 'qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty', 'quant_text'])[0]
            prod_data = json.dumps(prod_data)
            notifications.append(((self._cr.dbname, 'pos.sync.stock', self.env.user.id),
                                  {'id': rec.product_id.ids, 'prod_data': prod_data}, []))

        if len(notifications) > 0:
            self.env['bus.bus']._sendmany(notifications)
        return res

    def write(self, vals):
        res = super(StockQuant, self).write(vals)
        notifications = []
        for rec in self:
            prod_data = rec.product_id.read(
                ['id', 'qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty', 'quant_text'])[0]
            prod_data = json.dumps(prod_data)
            notifications.append(((self._cr.dbname, 'pos.sync.stock', self.env.user.id),
                                  {'id': rec.product_id.ids, 'prod_data': prod_data}, []))

        if len(notifications) > 0:
            self.env['bus.bus']._sendmany(notifications)
        return res
