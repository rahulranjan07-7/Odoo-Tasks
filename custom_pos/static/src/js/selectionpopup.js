odoo.define('point_of_sale.LocSelection', function (require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    
    class LocSelection extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.state = useState({ selectedId: this.props.list.find((item) => item.isSelected) });
        }
        selectItem(itemId) {
            this.state.selectedId = itemId;
            this.confirm();
        }
        
        getPayload() {
            const selected = this.props.list.find((item) => this.state.selectedId === item.id);
            return selected && selected.item;
        }
    }
    LocSelection.template = 'LocSelection';
    LocSelection.defaultProps = {
        cancelText:'Cancel',
        title: 'Select',
        body: '',
        confirmKey: false,
    };

    Registries.Component.add(LocSelection);

    return LocSelection;
});
