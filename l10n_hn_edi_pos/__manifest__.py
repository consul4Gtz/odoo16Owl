
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': "NH PoS",
    'author': 'Vauxoo',
    'website': 'https://www.vauxoo.com',
    'license': 'LGPL-3',
    'category': 'Accounting/Localizations/EDI',
    'version': '15.0.1.0.1',
    'depends': ['point_of_sale', 'l10n_hn_edi'],
    'data': [
        'views/pos_config_view.xml',
        'views/pos_order_view.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'l10n_hn_edi_pos/static/src/js/**/*',
            'l10n_hn_edi_pos/static/src/xml/**/*',
        ],
    },
    'installable': True,
}
