from odoo import models, api, fields, _
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv.expression import AND, OR

class InheritPosSession(models.Model):
	_inherit = 'pos.session'

	def _pos_ui_models_to_load(self):
	    result = super()._pos_ui_models_to_load()
	    result.extend(['product.packaging'])
	    return result

	def _loader_params_product_packaging(self):
	    return {
	        'search_params': {
	            'domain': [],
	            'fields': [],
	        }
	    }

	def _get_pos_ui_product_packaging(self, params):
	    return self.env['product.packaging'].search_read(**params['search_params'])

	def _product_pricelist_item_fields(self):
		return [
				'id',
				'product_tmpl_id',
				'product_id',
				'pricelist_id',
				'price_surcharge',
				'price_discount',
				'price_round',
				'price_min_margin',
				'price_max_margin',
				'company_id',
				'currency_id',
				'date_start',
				'date_end',
				'compute_price',
				'fixed_price',
				'percent_price',
				'base_pricelist_id',
				'base',
				'categ_id',
				'min_quantity',
				'applied_on',
				'product_package_id',
				'package_id',
				]

	def _loader_params_product_product(self):
		domain = [
			'&', '&', ('sale_ok', '=', True), ('available_in_pos', '=', True), '|',
			('company_id', '=', self.config_id.company_id.id), ('company_id', '=', False)
		]
		if self.config_id.limit_categories and self.config_id.iface_available_categ_ids:
			domain = AND([domain, [('pos_categ_id', 'in', self.config_id.iface_available_categ_ids.ids)]])
		if self.config_id.iface_tipproduct:
			domain = OR([domain, [('id', '=', self.config_id.tip_product_id.id)]])

		return {
			'search_params': {
				'domain': domain,
				'fields': [
					'packaging_ids','display_name', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id', 'barcode',
					'default_code', 'to_weight', 'uom_id', 'description_sale', 'description', 'product_tmpl_id','tracking',
					'write_date', 'available_in_pos', 'attribute_line_ids', 'active','__last_update', 'image_128'
				],
				'order': 'sequence,default_code,name',
			},
			'context': {'display_default_code': False},
		}
	


