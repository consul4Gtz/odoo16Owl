from odoo import _, api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    l10n_hn_edi_sag = fields.Char('Sag Register')
    l10n_hn_edi_exempt_order = fields.Char('Exempt Order')
    l10n_hn_edi_exempt_certificate = fields.Char('Exempt Certificate')
    l10n_hn_edi_diplomatic = fields.Char('Carnet de Diplomatico')
    l10n_hn_edi_number_receipt_refund = fields.Char('Number Receipt Refund')

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        if 'l10n_hn_edi_sag' in ui_order:
            res['l10n_hn_edi_sag'] = ui_order.get('l10n_hn_edi_sag')
        if 'l10n_hn_edi_diplomatic' in ui_order:
            res['l10n_hn_edi_diplomatic'] = ui_order.get('l10n_hn_edi_diplomatic')
        if 'l10_hn_exempt_purchase' in ui_order:
            res['l10n_hn_edi_exempt_order'] = ui_order.get('l10_hn_exempt_purchase')
        if 'l10n_hn_exempted_proof' in ui_order:
            res['l10n_hn_edi_exempt_certificate'] = ui_order.get('l10n_hn_exempted_proof')
        if 'l10n_hn_edi_number_receipt_refund' in ui_order:
            res['l10n_hn_edi_number_receipt_refund'] = ui_order.get('l10n_hn_edi_number_receipt_refund')
        return res

    def _prepare_invoice_vals(self):
        res = super()._prepare_invoice_vals()
        name = res.get('ref', '').replace(_(' REFUND'), '')
        document_number = self.name.replace(_(' REFUND'), '')
        if res.get('move_type') == 'out_invoice':
            res['l10n_latam_document_type_id'] = self.env.ref('l10n_hn_edi.sar_fact').id
            res['l10n_hn_edi_cai_id'] = self.config_id.l10n_hn_edi_cai_id.id
        elif res.get('move_type') == 'out_refund':
            res['l10n_latam_document_type_id'] = self.env.ref('l10n_hn_edi.sar_nc').id
            res['l10n_hn_edi_cai_id'] = self.config_id.l10n_hn_edi_refund_cai_id.id
            name = self.l10n_hn_edi_number_receipt_refund or name
            document_number = self.l10n_hn_edi_number_receipt_refund or document_number
        res['name'] = name
        res['l10n_latam_document_number'] = document_number
        res['l10n_hn_edi_from_pos'] = True
        res['l10n_hn_edi_sag'] = self.l10n_hn_edi_sag
        res['l10n_hn_edi_diplomatic_number'] = self.l10n_hn_edi_diplomatic
        res['l10n_hn_edi_exempt_order'] = self.l10n_hn_edi_exempt_order
        res['l10n_hn_edi_exempt_certificate'] = self.l10n_hn_edi_exempt_certificate
        return res

    def action_create_invoice(self):
        """When is created a new register, create automatically the invoice."""
        for order in self.filtered(lambda ord: not ord.account_move and ord.l10n_hn_edi_is_required()):
            order.action_pos_order_invoice()

    def action_validate_invoice(self):
        """Validate the invoice after of opened."""
        self.mapped('account_move').filtered(lambda inv: inv.state == 'draft').action_post()

    def action_pos_order_paid(self):
        """Create Invoice if company is HN"""
        res = super().action_pos_order_paid()
        if not self.partner_id:
            self.write({
                'partner_id': self.company_id.l10n_hn_edi_pos_default_partner_id.id
            })
        self.action_create_invoice()
        self.filtered(lambda r: r.account_move.state == 'draft').action_validate_invoice()
        return res

    def l10n_hn_edi_is_required(self):
        self.ensure_one()
        return self.company_id.country_id == self.env.ref('base.hn')
