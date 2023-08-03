{
    'name': 'School Management',
    'version': '16.0',
    'depends': ['base', 'mail', 'sale_management'],
    'author': 'Rahul Ranjan',
    'sequence': '1',
    'category': 'Education System',
    'description': 'storing students information',
    'website': 'https://www.smschool.com',
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_school_info_view.xml',
        'views/school.xml',
        'views/payment_view.xml',
        'views/salesmodel.xml',
        'views/demo.xml',
        'views/res_config_views.xml',
        'reports/student_card.xml',
        'reports/inherit.xml',
        'reports/report.xml',
        'data/mail_template.xml',
        'data/student_cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
