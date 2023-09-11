odoo.define('point_of_sale.phone_number', function(require) {
    'use strict';
 
    var { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    
    const CustomerPhoneNum = (Order) => class CustomerPhoneNum extends Order {

        export_for_printing(){
            var result = super.export_for_printing(...arguments);
            result.phoneNumber = this.get_customer_phone_number();
            return result;
        }
    }

    

    Registries.Model.extend(Order, CustomerPhoneNum);

    return CustomerPhoneNum;
});