from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_hn_edi_from_pos = fields.Boolean(
        'Created from PoS?', help='Helper to identify when the invoice was created from a PoS.')

    def l10n_hn_edi_resequence_is_required(self):
        """If the invoice comes from a PoS, is not necessary sequence"""
        if self.l10n_hn_edi_from_pos:
            return False
        return super().l10n_hn_edi_resequence_is_required()
