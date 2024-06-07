# -*- coding: utf-8 -*-
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
    'version': "16.0.1.0.1",
    'depends': ['sale_stock'],
    'data': [
        'views/sale_view.xml',
        'views/stock_location_view.xml',
    ],
    'installable': True,
    'assets': {
         'web.assets_backend': [
            'sale_stock_by_warehouse/static/src/**/*',
            ('remove', 'sale_stock_by_warehouse/static/src/legacy/**/*'),
        ],
        "web.assets_backend_legacy_lazy": [
            'sale_stock_by_warehouse/static/src/legacy/**/*',
        ]
    },
}
# legacy widgets v15 to v16