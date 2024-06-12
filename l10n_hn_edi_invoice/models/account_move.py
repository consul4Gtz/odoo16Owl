# -*- coding: utf-8 -*-
from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_hn_pr_edi_cai_id = fields.Many2one('l10n_hn_edi.cai', string='Clave de autorización CAI', copy=False, tracking=True, ondelete='restrict')
    authorization_date = fields.Date(string='Fecha de inicio')
    authorization_end_date = fields.Date(string='Fecha Final')
    l10n_hn_min_range_number = fields.Integer(string='Rango inicial')
    l10n_hn_max_range_number = fields.Integer(string='Rango máximo')
    is_purchase_receipt = fields.Boolean(string='Es Boleta de Compra', related='journal_id.is_purchase_receipt')

    def action_post(self):
        posted_before = self.read(['posted_before'])
        result = super().action_post()
        for move in self.filtered(lambda m: m.journal_id.is_purchase_receipt and m.country_code == 'HN' and
                                  m.move_type in ['in_invoice', 'in_refund']):
            record_posted_before = False
            for record in posted_before:
                if record.get('id') == move.id:
                    record_posted_before = record.get('posted_before')
                    continue
            # Increase sequence number for specific document type
            if not record_posted_before:
                doc_type = move.l10n_hn_edi_get_doc_type()
                sequence = move.journal_id.purchase_receipt_sequence_id
                if not sequence:
                    continue
                sequence.next_by_id()
        return result

    def _post(self, soft=True):
        moves = self.filtered(lambda m: m.journal_id.is_purchase_receipt and m.country_code == 'HN' and
                              m.move_type in ['in_invoice', 'in_refund'])
        for move in moves:
            move.name = move._l10n_hn_pr_edi_set_next_sequence()
        result = super()._post(soft=soft)
        
        for move in moves:
            sequence = move.journal_id.purchase_receipt_sequence_id
            if not sequence:
                continue
            cai_id = sequence.l10n_hn_edi_cai_id
            move._l10n_hn_edi_validations(sequence)

            move.l10n_hn_pr_edi_cai_id = cai_id
            move.authorization_date = cai_id.authorization_date
            move.authorization_end_date = cai_id.authorization_end_date
            move.l10n_hn_min_range_number = sequence.l10n_hn_min_range_number
            move.l10n_hn_max_range_number = sequence.l10n_hn_max_range_number
        return result

    def set_name_purchase_receipt(self):
        if self.is_purchase_receipt:
            sequence_id = self.journal_id.purchase_receipt_sequence_id
            sequence = "%s%s" % (sequence_id.prefix, str(sequence_id.number_next_actual).zfill(sequence_id.padding))
            # _logger.error("sequence onchange journal :%s", sequence)
            self.name = sequence

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        super(AccountMove, self)._onchange_journal_id()
        self.set_name_purchase_receipt()

    def _l10n_hn_pr_edi_set_next_sequence(self):
        sequence_id = self.journal_id.purchase_receipt_sequence_id
        if sequence_id:
            sequence = "%s%s" % (sequence_id.prefix, str(sequence_id.number_next_actual).zfill(sequence_id.padding))
            # _logger.error("sequence :%s", sequence)
            return sequence
        return ""

    def _get_starting_sequence(self):
        # OVERRIDE
        if self.is_purchase_receipt and self.journal_id:
            return self._l10n_hn_pr_edi_set_next_sequence()
        return super()._get_starting_sequence()

    def _get_sequence_format_param(self, previous):
        # OVERRIDE
        if not self or not self.is_purchase_receipt:
            return super()._get_sequence_format_param(previous)

        sequence_id = self.journal_id.purchase_receipt_sequence_id
        if not self.l10n_hn_edi_temp_sequence or self.l10n_hn_edi_temp_sequence < sequence_id.number_next_actual:
            self.l10n_hn_edi_temp_sequence = sequence_id.number_next_actual

        format_values = {
            'prefix1': f'{sequence_id.prefix}',
            'seq': self.l10n_hn_edi_temp_sequence,
            'suffix': '',
            'seq_length': sequence_id.padding,
            'year_length': 0,
            'year': 0,
            'month': 0,
            'year_end': 0,
            'year_end_length': 0,
        }
        return '{prefix1}{seq:0{seq_length}d}{suffix}', format_values