# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from odoo.tools import float_is_zero
import json
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class ProductProduct(models.Model):
    _inherit = 'product.product'

    quant_text = fields.Text('Quant Qty', compute='_compute_avail_locations', store=True)

    @api.depends('stock_quant_ids', 'stock_quant_ids.product_id', 'stock_quant_ids.location_id',
                 'stock_quant_ids.quantity')
    def _compute_avail_locations(self):
        notifications = []
        for rec in self:
            final_data = {}
            rec.quant_text = json.dumps(final_data)
            if rec.type == 'product':
                quants = self.env['stock.quant'].sudo().search(
                    [('product_id', 'in', rec.ids), ('location_id.usage', '=', 'internal')])
                outgoing = self.env['stock.move'].sudo().search(
                    [('product_id', '=', rec.id), ('state', 'not in', ['done']),
                     ('location_id.usage', '=', 'internal'),
                     ('picking_id.picking_type_code', 'in', ['outgoing'])])
                incoming = self.env['stock.move'].sudo().search(
                    [('product_id', '=', rec.id), ('state', 'not in', ['done']),
                     ('location_dest_id.usage', '=', 'internal'),
                     ('picking_id.picking_type_code', 'in', ['incoming'])])
                for quant in quants:
                    loc = quant.location_id.id
                    if loc in final_data:
                        last_qty = final_data[loc][0]
                        final_data[loc][0] = last_qty + quant.quantity
                    else:
                        final_data[loc] = [quant.quantity, 0, 0]

                for out in outgoing:
                    loc = out.location_id.id
                    if loc in final_data:
                        last_qty = final_data[loc][1]
                        final_data[loc][1] = last_qty + out.product_qty
                    else:
                        final_data[loc] = [0, out.product_qty, 0]

                for inc in incoming:
                    loc = inc.location_dest_id.id
                    if loc in final_data:
                        last_qty = final_data[loc][2]
                        final_data[loc][2] = last_qty + inc.product_qty
                    else:
                        final_data[loc] = [0, 0, inc.product_qty]

                rec.quant_text = json.dumps(final_data)
        return True
