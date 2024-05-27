# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.addons.account_edi.tests.common import AccountEdiTestCommon
from odoo.tests import tagged


@tagged('hn_edi_reports', 'post_install', '-at_install')
class HNReportSAR(AccountEdiTestCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref='l10n_hn.cuentas_plantilla', edi_format_ref=False):
        super().setUpClass(chart_template_ref=chart_template_ref, edi_format_ref=edi_format_ref)
        cls.sale_report = cls.env['l10n_hn.sar.libro']
        cls.partner = cls.env.ref('base.res_partner_2')
        cls.company = cls.env.user.company_id
        cls.company.country_id = cls.env.ref('base.hn')
        cls.date = fields.Datetime.context_timestamp(cls.company, fields.Datetime.from_string(fields.Datetime.now()))

    def test_001_generate_sale_report(self):
        """Generated a move with tax 15%."""
        invoice = self.generate_invoice()
        invoice.action_post()
        options = self.sale_report._get_options()
        date = self.date.replace(day=15).strftime('%Y-%m-%d')
        options.get('date', {})['date_from'] = date
        options.get('date', {})['date_to'] = date
        data = self.sale_report._get_lines(options)
        self.assertTrue(len(data) > 1, 'Lines not added correctly.')
        self.assertTrue(self.sale_report.get_xlsx(options))

    def test_002_generate_purchase_report(self):
        """Generated a move with tax 15% for purchase."""
        invoice = self.generate_invoice('in_invoice', 'purchase')
        invoice.action_post()
        options = self.sale_report._get_options()
        date = self.date.replace(day=15).strftime('%Y-%m-%d')
        options.get('date', {})['date_from'] = date
        options.get('date', {})['date_to'] = date
        data = self.sale_report._get_lines(options)
        self.assertTrue(len(data) > 1, 'Lines not added correctly.')
        self.assertTrue(self.sale_report.get_xlsx(options))

    def generate_invoice(self, invoice_type='out_invoice', journal_type='sale'):
        journal = self.env['account.journal'].search([
            ('type', '=', journal_type), ('company_id', '=', self.company.id)], limit=1)
        tax = self.env.ref('l10n_hn_edi.isv15' if journal_type == 'sale' else 'l10n_hn_edi.isc15').sudo()
        account = tax.invoice_repartition_line_ids.mapped('account_id').copy({'company_id': self.company.id})
        tax = tax.copy()
        tax.write({'company_id': self.company.id})
        (tax.invoice_repartition_line_ids | tax.refund_repartition_line_ids).write({
            'company_id': self.company.id, 'account_id': account.id,
        })
        invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': invoice_type,
            'invoice_date': self.date.replace(day=15),
            'journal_id': journal.id,
            'invoice_line_ids': [(0, 0, {
                'quantity': 1,
                'price_unit': 100,
                'name': 'Product Test',
                'tax_ids': [(4, tax.id)],
            })]
        })
        return invoice
