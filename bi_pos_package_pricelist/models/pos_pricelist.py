from odoo import models, api, fields, _
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError

class InheritProductPricelistItem(models.Model):
	_inherit = 'product.pricelist.item'
	

	@api.onchange('package_id')
	def onchange_pack_id(self):
		if self.package_id :
			self.min_quantity = self.package_id.qty

	# @api.onchange('package_id')
	# @api.depends('applied_on', 'categ_id', 'product_tmpl_id', 'product_id', 'compute_price', 'fixed_price', \
	# 	'pricelist_id', 'percent_price', 'price_discount', 'price_surcharge','package_id','product_package_id')
	# def _get_pricelist_item_name_price(self):
	# 	res = super(InheritProductPricelistItem, self)._get_pricelist_item_name_price()
	# 	for item in self:
	# 		if item.product_package_id and item.package_id.display_name and item.applied_on == '4_package':
	# 			item.name = (item.product_package_id.name + "["+item.package_id.display_name+"]")

	@api.onchange('package_id')
	@api.depends('applied_on', 'categ_id', 'product_tmpl_id', 'product_id', 'compute_price', 'fixed_price', \
				 'pricelist_id', 'percent_price', 'price_discount', 'price_surcharge', 'package_id',
				 'product_package_id')
	def _compute_name_and_price(self):
		res = super(InheritProductPricelistItem, self)._compute_name_and_price()
		for item in self:
			if item.product_package_id and item.package_id.display_name and item.applied_on == '4_package':
				item.name = (item.product_package_id.name + "[" + item.package_id.display_name + "]")

	package_id = fields.Many2one(
		'product.packaging',
		string='Select Product Pack'
	)

	applied_on= fields.Selection(selection_add=[
			('4_package', 'Product Pack'),
		], string='Apply On', required=True, copy=False, tracking=True, ondelete={'4_package': lambda recs: recs.write({'applied_on': 'odoo'})})

	product_package_id = fields.Many2one(
		'product.product',
		string='Product', 
	)