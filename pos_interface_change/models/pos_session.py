# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv.expression import AND, OR


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        params = super(PosSession, self)._loader_params_product_product()
        params['search_params']['fields'].extend(['type','virtual_available', 'qty_available','incoming_qty','outgoing_qty','quant_text'])
        return params