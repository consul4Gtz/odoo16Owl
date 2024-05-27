from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    incluido_en_libros = fields.Boolean(string='Incluir en Libros')
