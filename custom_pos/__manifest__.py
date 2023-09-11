{
    'name': 'custom_pos',
    'version': '16.0',
    'summary': 'Module for POS',
    'description': 'Custom Pos Module',
    'sequence': '1',
    'author': 'Rahul Ranjan',
    'category': 'Sale',
    'depends': ['point_of_sale', 'base'], 
    'data': [
        'security/ir.model.access.csv',
        'views/custom_pos.xml',
        'views/PartnerDetails.xml',
        'views/location.xml',
        'views/posconfigview.xml',
    ],

    'assets': {
      'point_of_sale.assets': [
                               "custom_pos/static/src/**/*",
                            ],
    },


    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3'
}