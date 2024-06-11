import json
from odoo import api, fields, models, _
from odoo.tools import float_compare

class AccountTemplateHeader(models.Model):
    _name = "account.template.header"
    _description = "Account Template Header"

    name = fields.Char(string='Nombre de plantilla', required=True)
    code = fields.Char(string='Codigo')
    line_ids = fields.One2many('account.template.line', 'template_id', string='Lines')
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Moneda' , required=True)
    active = fields.Boolean(default=True, string="Activo")  # Nuevo campo para archivar
    reference = fields.Char(string='Referencia')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'El código de la plantilla debe ser único!'),  # Restricción para código único
    ]

    def toggle_active(self):
        for record in self:
            record.active = not record.active

    def apply_template_and_close(self):
        active_id = self.env.context.get('active_id')
        move = self.env['account.move'].browse(active_id)

        if move:
            move.template_id = self.id
            move.apply_selected_template(self.id)

        return {'type': 'ir.actions.act_window_close'}

class AccountTemplateLine(models.Model):
    _name = "account.template.line"
    _description = "Account Template Line"

    template_id = fields.Many2one('account.template.header', string='Plantilla', ondelete='cascade')
    account_id = fields.Many2one('account.account', string='Cuenta', required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente')
    tag = fields.Char(string='Etiqueta')
    base_amount = fields.Float(string='Valor Base')
    amount_currency = fields.Float(string='Valor en moneda')
    currency_id = fields.Many2one('res.currency', string='Moneda', related='template_id.currency_id', store=True, readonly=False)
    debit = fields.Float(string='Debito')
    credit = fields.Float(string='Credito')
    analytic_distribution = fields.Json(inverse="_inverse_analytic_distribution")
    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),
    )


    @api.onchange('base_amount', 'currency_id')
    def _compute_amount_currency(self):
        for line in self:
            if line.currency_id and line.template_id.company_id:
                company_currency = line.template_id.company_id.currency_id
                line.amount_currency = line.currency_id._convert(
                    line.base_amount, 
                    company_currency, 
                    line.template_id.company_id, 
                    fields.Date.context_today(self)
                )

    @api.onchange('amount_currency', 'currency_id')
    def _compute_debit_credit(self):
        for line in self:
            if line.currency_id:
                company_currency = line.template_id.company_id.currency_id
                balance = line.currency_id._convert(line.amount_currency, company_currency, line.template_id.company_id, fields.Date.context_today(self))
                line.debit = balance if balance > 0 else 0
                line.credit = -balance if balance < 0 else 0
            else:
                line.debit = line.amount_currency if line.amount_currency > 0 else 0
                line.credit = -line.amount_currency if line.amount_currency < 0 else 0

    def _inverse_analytic_distribution(self):
        pass

class AccountMove(models.Model):
    _inherit = "account.move"

    template_id = fields.Many2one('account.template.header', string='Plantilla')

    def button_select_template(self):
        return {
            'name': 'Select Template',
            'type': 'ir.actions.act_window',
            'res_model': 'account.template.header',
            'view_mode': 'tree',
            'view_id': self.env.ref('account_template.view_account_template_header_tree').id,
            'target': 'new',
            'context': {'active_id': self.id, 'selection_mode': False},
            'options': {'no_create': True}
        }

    def apply_selected_template(self, template_id):
        template = self.env['account.template.header'].browse(template_id)
        if template:
            self.line_ids = [(5,)]
            self.ref = template.reference
            lines = []
            for line in template.line_ids:
                values = {
                    'account_id': line.account_id.id,
                    'partner_id': line.partner_id.id,
                    'name': line.tag,
                    'amount_currency': line.amount_currency,
                    'currency_id': line.currency_id.id,
                    'analytic_distribution': line.analytic_distribution,
                }
                lines.append((0, 0, values))
            self.line_ids = lines


