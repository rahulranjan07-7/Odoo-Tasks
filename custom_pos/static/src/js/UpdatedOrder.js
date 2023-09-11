odoo.define('point_of_sale.UpdatedOrder', function(require) {
    'use strict';
 
    var { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const UpdatedOrder = (Order) => class UpdatedOrder extends Order {

        constructor() {
            super(...arguments);
            this.phoneNumber = this.phoneNumber || '';
        }

        init_from_JSON(json) {
            super.init_from_JSON(json);
            this.set_customer_phone_number(json.customer_phone_number);
        }

        export_as_JSON() {
            const json = super.export_as_JSON();
            json.customer_phone_number = this.get_customer_phone_number();
            return json;
        }

        set_customer_phone_number(number) {
            this.phoneNumber = number;
        }

        get_customer_phone_number() {
            return this.phoneNumber;
        }
    }

    Registries.Model.extend(Order, UpdatedOrder);

    return UpdatedOrder;
});