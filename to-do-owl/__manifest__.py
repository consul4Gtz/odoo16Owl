# -*- coding: utf-8 -*-
{
    'name': "to-do-owl",

    'summary': """ Desarollo de un módulo de tareas""",
    
    'secuence': -1,

    'description': """
        Modulo de tareas
    """,
    
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'OWL',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
        #'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    
}