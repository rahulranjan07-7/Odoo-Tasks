odoo.define('custom_pos', function(require) {
    'use strict';
 
<<<<<<< HEAD
    var { Order } = require('point_of_sale.models');
=======
    // var { Order } = require('point_of_sale.models');
    const { Gui } = require("point_of_sale.Gui");
    const { _lt } = require("@web/core/l10n/translation");
>>>>>>> 97a401ffd5157842a9b733b04e3b458daf76c645
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const PhoneNumberUpdated = (ProductScreen) => class extends ProductScreen{
        setup() {
            super.setup();
        }
<<<<<<< HEAD
=======


>>>>>>> 97a401ffd5157842a9b733b04e3b458daf76c645
        async onClick() {
            console.log("clicked")
            const selectedOrder = this.env.pos.get_order();
            const { confirmed, payload: phoneNumber } = await this.showPopup('PhoneNumberPopup',  {
                startingValue: selectedOrder.get_customer_phone_number(),
<<<<<<< HEAD
                title: this.env._t('Add Customer Phone Number'),
=======
                // title: _lt('Add Customer order note'),
>>>>>>> 97a401ffd5157842a9b733b04e3b458daf76c645
            });
            if (confirmed) {
                selectedOrder.set_customer_phone_number(phoneNumber);
            }
        }
<<<<<<< HEAD
    }

=======

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



>>>>>>> 97a401ffd5157842a9b733b04e3b458daf76c645
    
    PhoneNumberUpdated.template = 'PhoneNumberUpdated';
    Registries.Component.extend(ProductScreen, PhoneNumberUpdated);

    return PhoneNumberUpdated;

    
});