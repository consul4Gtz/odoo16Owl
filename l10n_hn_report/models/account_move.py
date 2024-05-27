from odoo import api, models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    gravado = fields.Float(compute='_compute_impt_detail', store=True, digits='Product Price')
    gravado15 = fields.Float(string='Gravado 15%', compute='_compute_impt_detail', store=True, digits='Product Price')
    gravado18 = fields.Float(string='Gravado 18%', compute='_compute_impt_detail', store=True, digits='Product Price')
    isv15 = fields.Float(string='Isv 15%', compute='_compute_impt_detail', store=True, digits='Product Price')
    isv18 = fields.Float(string='Isv 18%', compute='_compute_impt_detail', store=True, digits='Product Price')
    exe = fields.Float(string='Exento', compute='_compute_impt_detail', store=True, digits='Product Price')
    exo = fields.Float(string='Exonerado', compute='_compute_impt_detail', store=True, digits='Product Price')
    no_tax_def = fields.Float('Sin Ind. Impt.', compute='_compute_impt_detail', store=True, digits='Product Price')
    isvimp = fields.Float(string='ISV Importacion', compute='_compute_impt_detail', store=True, digits='Product Price')
    exeimp = fields.Float(string='EXE Importacion', compute='_compute_impt_detail', store=True, digits='Product Price')
    isvr10 = fields.Float(string='ISV R10%', compute='_compute_impt_detail', store=True, digits='Product Price')

    @api.depends('product_id', 'quantity', 'price_subtotal', 'price_unit', 'tax_ids', 'discount')
    def _compute_impt_detail(self):
        for record in self:
            if record.tax_ids.name == 'ISV 15%':
                record.isv15 = record.price_subtotal * 0.15
                record.gravado = record.price_subtotal
                record.gravado15 = record.price_subtotal
            if record.tax_ids.name == 'ISV 18%':
                record.isv18 = record.price_subtotal * 0.18
                record.gravado = record.price_subtotal
                record.gravado18 = record.price_subtotal
            if record.tax_ids.name in ('EXE', 'EXEIMP'):
                record.exe = record.price_subtotal
            if record.tax_ids.name == 'EXO':
                record.exo = record.price_subtotal
            if record.tax_ids.name == 'ISVIMP':
                record.isvimp = record.price_subtotal
            if record.tax_ids.name == 'EXEIMP':
                record.exeimp = record.price_subtotal
            if record.tax_ids.name == 'ISVR10%':
                record.isvr10 = record.price_subtotal
            if not record.tax_ids.name:
                record.no_tax_def = record.price_subtotal
            record.update({
                'isv15': record.isv15,
                'gravado': record.gravado,
                'gravado15': record.gravado15,
                'gravado18': record.gravado18,
                'isv18': record.isv18,
                'exe': record.exe,
                'exo': record.exo,
                'no_tax_def': record.no_tax_def,
                'isvimp': record.isvimp,
                'exeimp': record.exeimp,
                'isvr10': record.isvr10,
            })


class AccountMove(models.Model):
    _inherit = "account.move"

    isv15 = fields.Float(string='ISV15%', compute='_compute_margin', store=True, digits='Product Price')
    isv18 = fields.Float(string='ISV18%', compute='_compute_margin', store=True, digits='Product Price')
    gravado = fields.Float(compute='_compute_margin', store=True, digits='Product Price')
    gravado15 = fields.Float(string='Gravado 15%', compute='_compute_margin', store=True, digits='Product Price')
    gravado18 = fields.Float(string='Gravado 18%', compute='_compute_margin', store=True, digits='Product Price')
    exento = fields.Float(compute='_compute_margin', store=True, digits='Product Price')
    exonerado = fields.Float(compute='_compute_margin', store=True, digits='Product Price')
    no_tax_def = fields.Float(string='Sin Ind. Impt.', compute='_compute_margin', store=True, digits='Product Price')
    isvimp = fields.Float(string='ISV Importacion', compute='_compute_margin', store=True, digits='Product Price')
    exeimp = fields.Float(string='EXE Importacion', compute='_compute_margin', store=True, digits='Product Price')
    isvr10 = fields.Float(string='ISV R10%', compute='_compute_margin', store=True, digits='Product Price')

    # Compute Section
    @api.depends('invoice_line_ids', 'invoice_line_ids.price_subtotal')
    def _compute_margin(self):
        for record in self:
            record.update({
                'isv15': sum(record.mapped('invoice_line_ids.isv15')),
                'isv18': sum(record.mapped('invoice_line_ids.isv18')),
                'gravado': sum(record.mapped('invoice_line_ids.gravado')),
                'gravado15': sum(record.mapped('invoice_line_ids.gravado15')),
                'gravado18': sum(record.mapped('invoice_line_ids.gravado18')),
                'exento': sum(record.mapped('invoice_line_ids.exe')),
                'exonerado': sum(record.mapped('invoice_line_ids.exo')),
                'no_tax_def': sum(record.mapped('invoice_line_ids.no_tax_def')),
                'isvimp': sum(record.mapped('invoice_line_ids.isvimp')),
                'exeimp': sum(record.mapped('invoice_line_ids.exeimp')),
                'isvr10': sum(record.mapped('invoice_line_ids.isvr10')),
            })
