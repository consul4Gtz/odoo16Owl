# -*- coding: utf-8 -*-
{
    'name': "POS Interface | POS Theme | POS Display | POS Screen | POS Stock",

    'summary': """
    The module allows you to change the logo, change the color, change the product interface in the form of a list, change odoo default order view to table view, change the position of the product group, change the position of the function buttons, show stock quantity.
        """,

    'description': """
        The module allows you to change the logo, change the color, change the product interface in the form of a list, change odoo default order view to table view, change the position of the product group, change the position of the function buttons.
    """,

    'author': "Dev Happy",
    'website': "https://www.dev-happy.com",
    'category': 'Point of Sale',
    'version': '16.0.7',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'views/pos_config_view.xml',
    ],
    'qweb': [
        'static/src/xml/screens/ProductScreen/*.xml',
        'static/src/xml/screens/OrderScreen/*.xml',
        'static/src/xml/screens/Chrome.xml',
        'static/src/xml/screens/WidgetsScreen/*.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            '/pos_interface_change/static/src/css/pos.css',
            '/pos_interface_change/static/src/css/pos_category.scss',
            '/pos_interface_change/static/src/js/Chrome.js',
            '/pos_interface_change/static/src/js/screens/ProductScreen/ProductsWidget.js',
            '/pos_interface_change/static/src/js/screens/ProductScreen/ProductScreen.js',
            '/pos_interface_change/static/src/js/screens/ProductScreen/ProductsWidgetControlPanel.js',
            '/pos_interface_change/static/src/js/screens/PaymentScreen/PaymentScreen.js',
            'pos_interface_change/static/src/xml/screens/ProductScreen/*.xml',
            'pos_interface_change/static/src/xml/screens/OrderScreen/*.xml',
            'pos_interface_change/static/src/xml/screens/Chrome.xml',
            'pos_interface_change/static/src/xml/screens/WidgetsScreen/*.xml',
        ],
    },
    'live_test_url':'https://youtu.be/pyfSqbjyzLA',
    'images':['static/description/banner.gif'],
    'currency': 'EUR',

    'support':"dev.odoo.vn@gmail.com",
    'price': 99.99,
    'license': 'OPL-1',
}
