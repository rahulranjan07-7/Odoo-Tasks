odoo.define('custom_pos.PartnerDetailsEditInherit', function(require) {
    'use strict';
 
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    const { _t } = require('@web/core/l10n/translation');

    const InheritPartnerDetailsEdit = (PartnerDetailsEdit) => class InheritPartnerDetailsEdit extends PartnerDetailsEdit {

        setup() {
            super.setup();
            console.log(this.props.partner)
            this.changes.new_phone_number = this.props.partner.new_phone_number || '';
        }
        async saveChanges() {
            console.log(this.changes.new_phone_number)
            const available_data = await this.env.services.rpc({
                model: 'res.partner',
                method: 'search_read',
                args: [[['new_phone_number', '=', this.changes.new_phone_number], ["id", "!=", this.props.partner.id]]]
            });
       
            if (available_data.length > 0) {
                this.showPopup('ErrorPopup', {
                    title: _t('Alternate Phone Number'),
                    body: _t(`Entered alternate phone number is already given by ${available_data[0].name}!!`)
                });            
            }
            else{
                super.saveChanges()
            }
        }
    }

    
    Registries.Component.extend(PartnerDetailsEdit, InheritPartnerDetailsEdit);

    return InheritPartnerDetailsEdit;
});