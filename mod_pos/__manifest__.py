# -*- coding: utf-8 -*-
{
    'name': "POS custom button",

    'summary': """
        agg custom button.""",

    'description': """
        agg custom button.
    """,

    'author': "consul4gtz",
    'website': "",

    'category': 'Point of Sale',
    'version': '0.1',

    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            '/static/src/xml/OrderReceipt.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
