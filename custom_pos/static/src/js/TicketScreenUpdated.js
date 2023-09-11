odoo.define('custom_pos.Ticket', function(require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');
    const {useState} = owl;

    const CustomTicketScreen = (TicketScreen) =>
    class CustomTicketScreen extends TicketScreen {
        setup() {
            super.setup();
            const phone = this.env.pos.get_order().get_customer_phone_number();
            this.phno = useState({'num': phone})
            console.log(this.env.pos.get_order().get_customer_phone_number());
        }
    }



    Registries.Component.extend(TicketScreen, CustomTicketScreen);

    return CustomTicketScreen;
});