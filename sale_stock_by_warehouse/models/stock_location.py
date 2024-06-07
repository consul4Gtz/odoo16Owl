# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
logger = logging.getLogger(__name__)

class Location(models.Model):
    _inherit = 'stock.location'
    
    special_location = fields.Boolean(string="Ubicación Especial", help="No considera el stock en las lineas de venta")