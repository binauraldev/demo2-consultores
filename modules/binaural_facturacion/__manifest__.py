# -*- coding: utf-8 -*-
{
    'name': "binaural facturacion",

    'summary': """
       Modulo para el proceso de Facturacion, Retenciones etc """,

    'description': """
        Modulo para el proceso de Compra/Facturacion/Retenciones asi como Facturacion/Retenciones con manejo de multimonedas
    """,

    'author': "Binauraldev",
    'website': "https://binauraldev.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account','binaural_contactos_configuraciones', 'account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/config_sequence.xml',
        #'views/views.xml',
        #'views/templates.xml',
        'views/config_views.xml',
        'views/account_move_form_inh.xml',
        'views/account_move_search_inh.xml',
        'views/account_move_trees_inh.xml',
        'views/account_retention.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}
