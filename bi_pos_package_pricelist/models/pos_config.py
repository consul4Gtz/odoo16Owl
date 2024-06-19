# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError

class CustomPOS(models.Model):
	_inherit = 'pos.config'

	remove_orderline = fields.Boolean(
	    string='Remove Orderline',
	)

	customer_required = fields.Boolean(
	    string='Customer Is Required',
	)



class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	remove_orderline = fields.Boolean( string='Remove Orderline',related="pos_config_id.remove_orderline",readonly=False)

	customer_required = fields.Boolean( string='Customer Is Required', related="pos_config_id.customer_required",readonly=False)
