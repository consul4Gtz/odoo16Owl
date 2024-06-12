# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from odoo.tools import float_is_zero
import json
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class PosOrder(models.Model):
    _inherit = 'pos.order'

    location_id = fields.Many2one(
	    comodel_name='stock.location',
		related='config_id.x_stock_location_id',
		string="Location", store=True,
		readonly=True,
    )

