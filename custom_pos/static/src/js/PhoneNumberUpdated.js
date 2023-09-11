odoo.define('custom_pos', function(require) {
    'use strict';
 
    var { Order } = require('point_of_sale.models');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const PhoneNumberUpdated = (ProductScreen) => class extends ProductScreen{
        setup() {
            super.setup();
        }
        async onClick() {
            console.log("clicked")
            const selectedOrder = this.env.pos.get_order();
            const { confirmed, payload: phoneNumber } = await this.showPopup('PhoneNumberPopup',  {
                startingValue: selectedOrder.get_customer_phone_number(),
                title: this.env._t('Add Customer Phone Number'),
            });
            if (confirmed) {
                selectedOrder.set_customer_phone_number(phoneNumber);
            }
        }
    }

    
    PhoneNumberUpdated.template = 'PhoneNumberUpdated';
    Registries.Component.extend(ProductScreen, PhoneNumberUpdated);

    return PhoneNumberUpdated;

    
});