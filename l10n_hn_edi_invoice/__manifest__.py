# -*- coding: utf-8 -*-
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl).

{
    'name':'Numeración Boleta de compra HN',
    'author': 'Jhonny Martínez',
    'website': 'https://sysneo.pe',
    'license': 'LGPL-3',
    'category':'Accounting',
    'version':'16.0',
    'depends': [
        'base',
        'account',
        'l10n_hn_edi',
    ],
    'data' : [
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'reports/document_invoice_purchase.xml',
    ],
    'installable': True,
    'auto_install': False,
}