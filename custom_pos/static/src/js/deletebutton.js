odoo.define("deleteButton", function (require) {
    "use strict";
  
    const Orderline = require("point_of_sale.Orderline");
    const Registries = require("point_of_sale.Registries");
  
    const OrderlineDelete = () =>
      class extends Orderline {
        setup() {
          super.setup();
        }
        async onClick(orderline) {
          const currentOrder = this.env.pos.get_order();
          currentOrder.remove_orderline(orderline);
        }
      };
    OrderlineDelete.template = "custom_pos.Orderline";
    Registries.Component.extend(Orderline, OrderlineDelete);
    return OrderlineDelete;
  });