from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_hn_edi_pos_default_partner_id = fields.Many2one(
        'res.partner', related='company_id.l10n_hn_edi_pos_default_partner_id', readonly=False,
        help='Default partner to be used when the order has not set the partner, this to allow invoice.')
