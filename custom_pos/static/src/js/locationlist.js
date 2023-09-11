odoo.define("pos_order.LocationList", function (require) {
    "use strict";
    const ProductScreen = require("point_of_sale.ProductScreen");
    const PosComponent = require('point_of_sale.PosComponent');
    const { useListener } = require("@web/core/utils/hooks");

    const Registries = require("point_of_sale.Registries");

    class LocationList extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
            this.all_order = this.env.pos.get_order();
            this.locations_from_config = this.env.pos.locations.filter(method => this.env.pos.config.loc_selection.includes(method.id));

        }
        get pre_select_location(){
            if (this.all_order.loc_selection){
                return this.all_order.loc_selection.id
            }
            return false
        }
        get selected_loc(){
            let loc = this.all_order.get_location()
            return loc ? loc.location : false
        }
        async onClick() {
            const selectedList = this.locations_from_config.map(locationlist => ({
                id: locationlist.id,
                label: locationlist.location,
                isSelected: locationlist.id === this.pre_select_location,
                item: locationlist,
            }));

            const { confirmed, payload: selectedLocation } = await this.showPopup(
                'LocationPopup',
                {
                    list: selectedList,
                }
            );

            if (confirmed) {
                this.all_order.set_location(selectedLocation);
            }

        }
    }

    ProductScreen.addControlButton({
        component: LocationList,
    })
    
    LocationList.template = 'LocationList';
    Registries.Component.add(LocationList);
}); 