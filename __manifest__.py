# -*- coding: utf-8 -*-
{
    'name': "Africa Transit",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'transit',
    'version': '15.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'sale',
                'crm',
                ],

    # always loaded
    'data': [
        'security/ccbmtransit_security.xml',
        'security/ir.model.access.csv',
        'views/partner_views.xml',
        'views/dossier_views.xml',
        'views/transit_service_views.xml',
        'views/transit_users_views.xml',
        'views/transit_menu_views.xml',
        'data/dossier_stage.xml'
    ]
}
