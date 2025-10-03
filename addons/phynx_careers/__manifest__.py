# -*- coding: utf-8 -*-
{
    'name': "phynx_careers",

    'summary': "Phynx Careers is a Ugandan education consultancy company",

    'description': """
Track applicants and phynx career operations
    """,

    'author': "TechAccess",
    'website': "https://techaccess.tech",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'hr_recruitment',
                'web',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner.xml',
        'views/recruitment.xml',
        'views/cv_report.xml',
        'views/register.xml',
        'data/ir_sequence_data.xml',
        'views/cover_letter.xml',
        'views/crm_lead.xml',
        #'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'assets': {
    'web.assets_backend': [
        'phynx_careers/static/**/*',
        'phynx_careers/static/src/css/custom.css'
    ],
    },
}

