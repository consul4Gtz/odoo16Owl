{
    'name': 'Generador de Plantillas de Asiento',
    'version': '1.0',
    'author': 'IT SOLUTIONS S. DE R.L.',
    'application_icon': 'account_template/static/description/icon.png',
    'website': 'https://www.itechnologysol.com',
    'category': 'Accounting',
    'summary': 'Crear plantillas de asientos contables, para ser utilizadas como base en la creacion de asientos contables manuales.',
    'depends': ['account', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        #'data/menu_data.xml',
        'views/account_template_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
