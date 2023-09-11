odoo.define("pos_order.LocationPopup", function (require) {
    "use strict";
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const { useState } = owl;
    const Registries = require("point_of_sale.Registries");
    const { _lt } = require('@web/core/l10n/translation');
    const { Order } = require("point_of_sale.models");

    class LocationPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.state = useState({ selected_loc: this.props.list.find((item) => item.isSelected) });
        }
        selectItem(itemId) {

            this.state.selected_loc = itemId;
            this.confirm();
        }

        getPayload() {
            const selected = this.props.list.find((item) => this.state.selected_loc === item.id);
            return selected && selected.item;
        }
    }
    LocationPopup.template = "LocationPopup_template"
    LocationPopup.defaultProps = {
        cancelText: _lt('Cancel'),
        title: _lt('Select Location'),
        body: '',
        list: [],
        confirmKey: false,
    }
    Registries.Component.add(LocationPopup)

    const OrderExtendLocation = (Order) => class OrderExtendLocation extends Order {

        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.loc_selection = this.loc_selection;
            return json;
        }

        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.set_location(json.loc_selection)
        }

        set_location(loc_selection) {
            this.loc_selection = loc_selection
        }

        get_location() {
            if (this.loc_selection) {
                return this.loc_selection;
            }
        }
    }

    Registries.Model.extend(Order, OrderExtendLocation)

});