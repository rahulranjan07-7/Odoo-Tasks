odoo.define('custom_pos', function(require) {
    'use strict';
 
    const { Gui } = require("point_of_sale.Gui");
    const { _lt } = require("@web/core/l10n/translation");
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
                title: _lt('Add Customer order note'),
            });
            if (confirmed) {
                selectedOrder.set_customer_phone_number(phoneNumber);
            }
        }

        async _onClickPay() {
            console.log(this.env.pos.get_order().partner);
            if (this.env.pos.get_order().partner == null) {
              Gui.showPopup("ErrorPopup", {
                title: _lt("Error"),
                body: _lt(`You need to select customer to go ahead with the process!!`),
              });
            } else {
              super._onClickPay();
            }
          }
    }

    PhoneNumberUpdated.template = 'PhoneNumberUpdated';
    Registries.Component.extend(ProductScreen, PhoneNumberUpdated);

    return PhoneNumberUpdated;
    
});