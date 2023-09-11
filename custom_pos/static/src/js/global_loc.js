odoo.define("pos_training.PosGlobalLoc", function (require) {
    'use strict';
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require("point_of_sale.Registries");

    const PosGlobalLoc = (PosGlobalState) => class extends PosGlobalState {
        async _processData(loadedData) {
            this.locations = loadedData['pos.location']
            super._processData(loadedData)
        }
    }
    Registries.Model.extend(PosGlobalState, PosGlobalLoc);
});