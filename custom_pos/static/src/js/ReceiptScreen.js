odoo.define('point_of_sale.UpdatedOrder', function(require) {
    'use strict';
 
    var { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const UpdatedOrder = (Order) => class UpdatedOrder extends Order {

        constructor() {
            super(...arguments);
           
        }

        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.set_customer_phone_number(json.customer_phone_number);
        }

        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.customer_phone_number = this.customer_phone_number;
            return json;
        }

        set_customer_phone_number(number) {
            this.customer_phone_number = number;
        }

        get_customer_phone_number() {
            return this.customer_phone_number;
        }
        export_for_printing(){
            const note=super.export_for_printing(...arguments);
            if(this.get_customer_phone_number()){
            note.customer_phone_number=this.get_customer_phone_number();
            }
            return note;
        }
    }

    Registries.Model.extend(Order, UpdatedOrder);

    return UpdatedOrder;
});