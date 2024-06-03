# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_config(self):
        result = super()._loader_params_pos_config()
        # result['search_params']['fields'] += ['l10n_hn_initial_fiscal_correlative', 'l10n_hn_final_fiscal_correlative', 'l10n_hn_edi_authorization_date', 'l10n_hn_edi_authorization_end_date', 'number_next_actual', 'number_next_actual_refund']
        # result['search_params']['fields'].extend(['l10n_hn_initial_fiscal_correlative', 'l10n_hn_final_fiscal_correlative', 'l10n_hn_edi_authorization_date', 'l10n_hn_edi_authorization_end_date', 'number_next_actual', 'number_next_actual_refund'])
        result['search_params']['fields'].append('number_next_actual')
        # result['search_params']['fields'].append('l10n_hn_final_fiscal_correlative')
        return result
