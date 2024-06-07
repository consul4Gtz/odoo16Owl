# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _

import logging
logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id')
    def _get_stock_info_JSON(self):
        for res in self:
            if res.product_id:

                info = {'title': 'Stock Disponible por Almacen', 'outstanding': False, 'content': []}

                warehouses = self.env['stock.warehouse'].sudo().search([('company_id','=',self.env.company.id)])

                default = False
                for wh in warehouses:
                    loc = []
                    
                    domain = [
                        ('location_id', 'child_of', wh.lot_stock_id.location_id.id), 
                        ('product_id', '=', res.product_id.id),
                        ('location_id.special_location', '=', False)
                    ]

                    quants = self.env['stock.quant'].sudo().search(domain)
                    # quants = quants.sudo().filtered(lambda r: r.location_id.special_location == False)

                    if quants:
                        stock_real = sum(quants.mapped('quantity')) or 0.0
                        stock_reserved = sum(quants.mapped('reserved_quantity')) or 0.0
                        if (stock_real - stock_reserved) > 0:
                            info['content'].append({
                                'name': wh.name,
                                'default': default,
                                #'journal_name': self.order_id.warehouse_id.name,
                                'stock_real': stock_real,
                                'stock_reserved': stock_reserved,
                                'stock_disponible': stock_real - stock_reserved,
                                #'ubicaciones':ubica
                            })
                #logger.error('infoooo: %s', info)
                res.sale_line_stock_widget = json.dumps(info)
            else:
                res.sale_line_stock_widget = json.dumps(False)


   sale_line_stock_widget = fields.Text("Stock", compute='_get_stock_info_JSON', readonly=True)
    #campo extra para qque muestre el widget
    widget = fields.Text("Stock", readonly=False)
    # sale_line_stock_widget_text = fields.Char(string="Stocks",compute="Test" )

