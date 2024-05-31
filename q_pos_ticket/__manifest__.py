# -*- coding: utf-8 -*-
# Copyright 2022 - QUADIT, SA DE CV (https://www.quadit.mx)
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Add Internal Reference to PoS Ticket',
    'category': 'Point of Sale',
    'summary': 'Add default code to pos ticket and screen widget.',
    'version': '16.0.0.0.1',
    'license': 'OPL-1',
    'author': 'QUADIT',
	'support': 'support@quadit.mx',
    'website' : 'https://www.quadit.mx',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'q_pos_ticket/static/src/js/models.js',
            'q_pos_ticket/static/src/scss/style.scss',
        ],
        'web.assets_qweb': [
            'q_pos_ticket/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': False,
}
