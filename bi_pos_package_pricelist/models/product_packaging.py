# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    barcode_2 = fields.Char('Barcode 2', copy=False,)
    barcode_3 = fields.Char('Barcode 3', copy=False,)
    barcode_4 = fields.Char('Barcode 4', copy=False,)

    @api.constrains('barcode')
    def _check_barcode_1_uniqueness(self):
        for record in self:
            if record.barcode:
                domain = ['|','|',('barcode_2','=',record.barcode),('barcode_3','=',record.barcode),('barcode_4','=',record.barcode)]
                if self.env['product.packaging'].search(domain, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))

    @api.constrains('barcode_2')
    def _check_barcode_2_uniqueness(self):
        for record in self:
            if record.barcode_2:
                domain = ['|','|',('barcode','=',record.barcode_2),('barcode_3','=',record.barcode_2),('barcode_4','=',record.barcode_2)]
                domain_prod = [('barcode','=',record.barcode_2)]
                if self.env['product.packaging'].search(domain, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))
                if self.env['product.product'].search(domain_prod, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))

    @api.constrains('barcode_3')
    def _check_barcode_3_uniqueness(self):
        for record in self:
            if record.barcode_3:
                domain = ['|','|',('barcode','=',record.barcode_3),('barcode_2','=',record.barcode_3),('barcode_4','=',record.barcode_3)]
                domain_prod = [('barcode','=',record.barcode_3)]
                if self.env['product.packaging'].search(domain, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))
                if self.env['product.product'].search(domain_prod, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))

    @api.constrains('barcode_4')
    def _check_barcode_4_uniqueness(self):
        for record in self:
            if record.barcode_4:
                domain = ['|','|',('barcode','=',record.barcode_4),('barcode_2','=',record.barcode_4),('barcode_3','=',record.barcode_4)]
                domain_prod = [('barcode','=',record.barcode_4)]
                if self.env['product.packaging'].search(domain, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))
                if self.env['product.product'].search(domain_prod, order="id", limit=1):
                    raise ValidationError(_("A product already uses the barcode"))


	





	



