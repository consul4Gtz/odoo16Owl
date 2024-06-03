from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_hn_edi_pos_default_partner_id = fields.Many2one(
        'res.partner', help='Default partner to be used when the order has not set the partner, this to allow invoice.'
    )
