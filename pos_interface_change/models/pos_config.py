# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'


    def _get_default_location(self):
        return self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)],
                                                  limit=1).lot_stock_id
    x_display_product_list = fields.Boolean('Mostrar productos como una lista', default=False)
    x_display_order_list = fields.Boolean('Mostrar tabla de pedidos', default=False)
    x_background_color = fields.Char('Color de fondo', default='#865a7b', required=True)
    x_logo = fields.Image('Logotipo punto de venta')
    x_position_categories = fields.Selection([('default','Por defecto'),('right','Derecha'), ('bottom','Abajo')], 'Categorías Posición', default='default',required=True)
    x_toggle_numpad = fields.Boolean('Alternar teclado numérico', default=False)
    x_position_button = fields.Selection([('default','Por defecto'),('left','Izquierda'),('right','Derecha')],'Posición del botón', default='default',required=True)
    #POS Stock
    x_pos_display_stock = fields.Boolean(string='Mostrar stock en POS')
    x_pos_stock_type = fields.Selection(
        [('onhand', 'Cantidad disponible'), ('incoming', 'Cantidad entrante'), ('outgoing', 'Cantidad saliente'),
         ('available', 'Cantidad disponible')], string='Tipo de acción', help='El vendedor puede mostrar diferentes tipos de stock en el POS.')
    x_pos_allow_order = fields.Boolean(string='Permitir pedidos en POS cuando el producto está agotado')
    x_pos_deny_order = fields.Char(string='Denegar pedido pos')
    x_show_stock_location = fields.Selection([
        ('all', 'Todo el almacén'),
        ('specific', 'Almacén de sesión actual'),
    ], string='Mostrar existencias de ', default='all')
    x_stock_location_id = fields.Many2one(
        'stock.location', string='Ubicación del inventario',
        domain=[('usage', '=', 'internal')], required=True, default=_get_default_location)
    #End Pos Stock
