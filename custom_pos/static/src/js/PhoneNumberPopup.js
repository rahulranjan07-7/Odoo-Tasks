odoo.define('custom_pos.PhoneNumberPopup', function (require) {
    'use strict';
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    // const models = require('point_of_sale.models')
    const Registries = require('point_of_sale.Registries');
    const { useState, useRef } = owl;
    const { _lt } = require('@web/core/l10n/translation');

    class PhoneNumberPopup extends AbstractAwaitablePopup {
        /**
         * @param {Object} props
         * @param {string} props.startingValue
         */
        setup() {
            super.setup();
            this.state =  useState({ inputValue: this.props.startingValue });
            this.phoneNumber = useRef('phoneNumber');
            
            this.phone = useState({
                error: '',
            }); 
        }

        getPayload() {
            return this.state.inputValue;
        }

        confirm(){
            const phno = this.phoneNumber.el.value
           
            if (phno == ""){
                this.phone.error="Order Note"
            }
            else{
                this.phone.error="Enter valid note"
                return super.confirm();
            }
        }
    }
    PhoneNumberPopup.template = 'custom_pos.PhoneNumberPopup';
    PhoneNumberPopup.defaultProps = {
        confirmText: _lt('Confirm'),
        cancelText: _lt('Cancel'),
    }

    Registries.Component.add(PhoneNumberPopup);

    return PhoneNumberPopup;

});