# -*- coding:utf-8 -*-
from odoo import _, api, models
from odoo.tools import formatLang, format_date

class L10nHNSarCompra(models.Model):
    _name = "l10n_hn.sar.libro.compras"
    _inherit = "account.report.custom.handler"
    _description = "Libro de Compras"

    def _dynamic_lines_generator(self, report, options, all_column_groups_expression_totals, warnings=None):
        data_lines = self._get_lines(options, None)
        lines = [(0, line) for line in data_lines]
        return lines

    @api.model
    def _get_lines(self, options, line_id=None):
        context = self.env.context
        journal_type = options.get('journal_type', 'purchase')
        date_from = options['date']['date_from']
        date_to = options['date']['date_to']
        empresa = options.get('selected_partner_ids')
        journal = options.get('name_journal_group')
        journals = options.get('journals')
        new_journals = []
        if journals:
            for line in journals:
                if line['type'] in ('sale', 'purchase'):
                    new_journals.append(line)
            options['journals'] = new_journals

        lines = []
        line_id = 0
        sign = 1.0 if journal_type == 'purchase' else 1.0

        totals = {}.fromkeys(['gravado15', 'gravado18', 'gravado', 'isvimp', 'exeimp', 'no_tax_def', 'exento', 
                              'exonerado', 'impuesto15', 'impuesto18', 'impuesto', 'total'], 0)
        domain = [('journal_id.type', '=', journal_type), ('company_id', '=', self.env.company.id)]
        domain += [('fecha', '>=', date_from), ('fecha', '<=', date_to)]
        if empresa:
            domain += [('empresa', 'in', empresa)]

        for rec in self.env['account.report.sar'].search_read(domain):
            totals['gravado15'] += rec['gravado15']
            totals['gravado18'] += rec['gravado18']
            totals['isvimp'] += rec['isvimp']
            totals['exeimp'] += rec['exeimp']
            totals['exento'] += rec['exento']
            totals['exonerado'] += rec['exonerado']
            totals['no_tax_def'] += rec['no_tax_def']
            totals['impuesto15'] += rec['impuesto15']
            totals['impuesto18'] += rec['impuesto18']
            totals['total'] += rec['total']

            if rec['type'] in ['in_invoice', 'in_refund']:
                caret_type = 'account.invoice.in'
            elif rec['type'] in ['out_invoice', 'out_refund']:
                caret_type = 'account.invoice.out'
            else:
                caret_type = 'account.move'

            # Redondeo de valores
            lines.append({
                'id': '~account.move~' + str(rec['id']),
                'name': format_date(self.env, rec['fecha']),
                'class': 'date',
                'level': 2,
                'model': 'account.report.sar',
                'caret_options': caret_type,
                'columns': [
                    {'name': rec['factura']},
                    {'name': rec['empresa'], 'class': 'whitespace_print'},
                    {'name': rec['rtn'], 'class': 'whitespace_print'},
                    {'name': formatLang(self.env, sign * rec['gravado15'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['gravado18'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['isvimp'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['exeimp'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * (rec['no_tax_def'] + rec['exento']), currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['exonerado'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['impuesto15'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['impuesto18'], currency_obj=self.env.company.currency_id)},
                    {'name': formatLang(self.env, sign * rec['total'], currency_obj=self.env.company.currency_id)},
                ],
            })
        line_id += 1

        # Redondeo de totales
        totals_rounded = {key: round(value, 2) for key, value in totals.items()}

        # Línea de Totales
        lines.append({
            'id': '~total~' + str(line_id),
            'name': _('Total'),
            'class': 'o_account_reports_domain_total',
            'level': 0,
            'columns': [
                {'name': ''},
                {'name': ''},
                {'name': ''},
                {'name': formatLang(self.env, totals_rounded['gravado15'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['gravado18'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['isvimp'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['exeimp'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['no_tax_def'] + totals_rounded['exento'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['exonerado'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['impuesto15'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['impuesto18'], currency_obj=self.env.company.currency_id)},
                {'name': formatLang(self.env, totals_rounded['total'], currency_obj=self.env.company.currency_id)},
            ],
        })

        return lines
