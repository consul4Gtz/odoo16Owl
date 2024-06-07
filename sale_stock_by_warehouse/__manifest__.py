# -*- coding: utf-8 -*-
{
    'name': "Stock por Ubicación en Ventas",
    'summary': "Stock por Ubicación en Ventas",
    'description': """
    
    Stock por Ubicación en las lineas de Venta.

    """,
    'author': "Javier Salazar Carlos",
    'website': "http://sysneo.pe",
    'category': '',
    'version': '0.1',
    'depends': ['sale_stock'],
    'data': [
        'views/sale_view.xml',
        'views/stock_location_view.xml',
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'sale_stock_by_warehouse/static/src/js/sale_line_stock_widget.js',
        ],
        'web.assets_qweb': [
            'sale_stock_by_warehouse/static/src/xml/**/*',
        ],
    },
}