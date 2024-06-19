# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "POS Package Based Pricelist",
    'version': '16.0.1.0',
    "category": "Point of Sales",
    'summary': 'This odoo app helps user to create, sell and manage point of sale product in multiple packages for same product with different quantity and different price option using pricelist. User can set different prices for various packages of the same product using the same pricelist. User can select available product packages of product in point of sale and also enter quantity of packages and can seen in POS receipt.',
    "description": """
    
            Point Of Sale Manage Packages with Pricelist in odoo,
            Manage Product Packages with using pricelist in odoo,
            Multiple Product Packages for the Same Product in odoo,
            Available Product Packages options in odoo,
            Product Packages show in POS receipt,
            Manage Product Package in POS in odoo,         
    
    """,
    "author": "BrowseInfo",
    "website": "https://www.browseinfo.com",
    "price": 49,
    "currency": 'EUR',
    "depends": ['base', 'stock', 'account', 'point_of_sale'],
    "data": [
        'views/pos_pricelist_view.xml',
        'views/pos_config.xml',
        'views/product_package_view.xml',
    ],
    'qweb': [
    ],
    'assets': {
        'point_of_sale.assets': [
            'bi_pos_package_pricelist/static/src/css/product_package_style.css',
            'bi_pos_package_pricelist/static/src/js/product_package.js',
            'bi_pos_package_pricelist/static/src/js/popup/Packagepopup.js',
            'bi_pos_package_pricelist/static/src/js/Screens/OrderWidget.js',
            'bi_pos_package_pricelist/static/src/js/model.js',
            'bi_pos_package_pricelist/static/src/js/pos_db.js',
            'bi_pos_package_pricelist/static/src/xml/product_pack.xml',
        ],
    },
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "live_test_url": 'https://youtu.be/VaLPhcQDRh0',
    "images": ["static/description/Banner.gif"],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
