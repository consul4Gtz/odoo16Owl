# Copyright 2021 Vauxoo
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'NH Fiscal Reports',
    'author': 'Its',
    'website': 'https://www.vauxoo.com',
    'license': 'LGPL-3',
    'category': 'Accounting/Localizations/EDI',
    'version': '16.0.1.0.0',
    'depends': [
        'account_reports',
        'l10n_hn_edi',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_sar_libro.xml',
        'views/sar_view.xml',
        'views/account_journals_view.xml',
    ],
    'installable': True,
}
