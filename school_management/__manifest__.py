{
'name': 'School Management',
'version': '16.0',
'author': 'Rahul Ranjan',
'depends': ['base', 'mail'],
'category': 'Education System',
'description': 'storing students information',
'website': 'https://www.smschool.com',
'data': [
        'security/ir.model.access.csv',
        'views/school.xml',
        'views/demo.xml',
        ],
        'installable': True,
        'application': True,
        'auto_install': False,   
}
