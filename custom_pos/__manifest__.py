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
<<<<<<< HEAD
        'views/inherit_pos_order_view.xml',
       
=======
        'views/partner_details.xml',
>>>>>>> 97a401ffd5157842a9b733b04e3b458daf76c645
    ],

    'assets': {
      'point_of_sale.assets': [
<<<<<<< HEAD
                               'custom_pos/static/src/js/OrderScreenUpdated.js',
                               'custom_pos/static/src/xml/OrderScreenUpdated.xml',
                               'custom_pos/static/src/js/override.js',
                               'custom_pos/static/src/js/PhoneNumberPopup.js',
                               'custom_pos/static/src/xml/PhoneNumberPopup.xml',
                               'custom_pos/static/src/js/PhoneNumberUpdated.js',
                               'custom_pos/static/src/xml/PhoneNumberPopup.xml',
                               'custom_pos/static/src/js/TicketScreenUpdated.js',
                               'custom_pos/static/src/xml/TicketScreenUpdated.xml',
                               'custom_pos/static/src/js/UpdatedOrder.js',
                               'custom_pos/static/src/xml/PhoneNumberUpdated.xml',
=======
                               'custom_pos/static/src/js/*',
                               'custom_pos/static/src/xml/*',
>>>>>>> 97a401ffd5157842a9b733b04e3b458daf76c645
                            ]
    },


    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
