# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountJournal(models.Model):
    _inherit = "account.journal"

    is_purchase_receipt = fields.Boolean(string='Es Boleta de Compra')
    purchase_receipt_sequence_id = fields.Many2one('ir.sequence', string='Secuencia Boleta de Compra')