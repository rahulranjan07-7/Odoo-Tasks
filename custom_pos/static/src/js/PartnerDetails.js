odoo.define('custom_pos.PartnerDetailsEditInherit', function(require) {
    'use strict';
 
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    const { _t } = require('@web/core/l10n/translation');

    const InheritPartnerDetailsEdit = (PartnerDetailsEdit) => class InheritPartnerDetailsEdit extends PartnerDetailsEdit {

        setup() {
            super.setup();
            console.log(this.props.partner.new_phone_number)
            this.changes.new_phone_number = this.props.partner.new_phone_number || '';
        }
    }

    
    Registries.Component.extend(PartnerDetailsEdit, InheritPartnerDetailsEdit);

    return InheritPartnerDetailsEdit;
});