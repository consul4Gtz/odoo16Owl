from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class PosConfig(models.Model):
    _inherit = "pos.config"

    l10n_hn_initial_fiscal_correlative = fields.Integer(
        string="Initial range", related="sequence_id.l10n_hn_min_range_number")
    l10n_hn_final_fiscal_correlative = fields.Integer(
        "Final range", related="sequence_id.l10n_hn_max_range_number")
    number_next_actual = fields.Integer(
        string="Next number",
        related="sequence_id.number_next_actual")
    prefix = fields.Char(related='sequence_id.prefix')
    padding = fields.Integer(related='sequence_id.padding')
    l10n_hn_edi_authorization_date = fields.Date(
        related='sequence_id.l10n_hn_edi_cai_id.authorization_date')
    l10n_hn_edi_authorization_end_date = fields.Date(
        related='sequence_id.l10n_hn_edi_cai_id.authorization_end_date')
    l10n_hn_edi_cai_id = fields.Many2one(related='sequence_id.l10n_hn_edi_cai_id', string='Invoice CAI')
    l10n_hn_edi_refund_cai_id = fields.Many2one(
        related='l10_hn_sequence_refund_id.l10n_hn_edi_cai_id', string="Refund CAI")
    l10n_hn_edi_sar_authorization_number = fields.Char(
        related='sequence_id.l10n_hn_edi_cai_id.name')
    l10n_hn_edi_sar_authorization_number_refund = fields.Char(
        'Refund CAI Name', related='l10_hn_sequence_refund_id.l10n_hn_edi_cai_id.name')
    l10_hn_number_receipt = fields.Char(compute='_compute_receipt_number')
    l10n_hn_edi_sag = fields.Char()
    l10_hn_exempt_purchase = fields.Char()
    l10n_hn_exempted_proof = fields.Char()
    is_refunded = fields.Boolean(default=False)
    l10_hn_sequence_refund_id = fields.Many2one('ir.sequence', string='Order Refund IDs Sequence')
    l10n_hn_edi_number_receipt_refund = fields.Char(compute='_compute_receipt_number_refund')
    number_next_actual_refund = fields.Integer(related="l10_hn_sequence_refund_id.number_next_actual")
    l10n_hn_final_fiscal_correlative_refund = fields.Integer(
        related="l10_hn_sequence_refund_id.l10n_hn_max_range_number")
    end_date_refund = fields.Date("Final Date Refund",
                                  related='l10_hn_sequence_refund_id.l10n_hn_edi_cai_id.authorization_end_date')
    prefix_refund = fields.Char("Prefix Refund", related='l10_hn_sequence_refund_id.prefix')

    #prueba de campos para sucursal
    sucursal_name = fields.Char(string='Branch', required=True, store=True)
    sucursal_adress = fields.Char()

    @api.constrains('sequence_id')
    def _check_sequence_settings(self):
        for config in self.filtered(lambda c: c.company_id.country_id == self.env.ref('base.hn') and
                                    c.sequence_id.l10n_hn_edi_cai_id):
            sequence = config.sequence_id
            if sequence.l10n_hn_max_range_number < sequence.number_next_actual:
                raise UserError(_('Fiscal correlative expired %s') % sequence.l10n_hn_max_range_number)
            date = fields.Datetime.context_timestamp(
                self.with_context(tz='America/Tegucigalpa'), fields.Datetime.now())
            if date.date() > sequence.l10n_hn_edi_cai_id.authorization_end_date:
                raise UserError(_('Fiscal date expired %s ') % (sequence.l10n_hn_edi_cai_id.authorization_end_date))

    @api.depends('prefix', 'number_next_actual', 'padding')
    def _compute_receipt_number(self):
        for record in self:
            self.l10_hn_number_receipt = "%s%s" % (
                record.prefix,
                str(record.number_next_actual - 1).zfill(record.padding),
            )

    @api.depends('prefix', 'number_next_actual', 'padding')
    def _compute_receipt_number_refund(self):
        if not self.l10_hn_sequence_refund_id:
            raise ValidationError(_("You must add a refund sequence."))
        for record in self.l10_hn_sequence_refund_id:
            self.l10n_hn_edi_number_receipt_refund = "%s%s" % (
                record.prefix,
                str(record.number_next_actual - 1).zfill(record.padding),
            )

    def get_next_document_number(self):
        number = self.l10_hn_sequence_refund_id.next_by_id()
        return number
