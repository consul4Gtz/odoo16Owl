odoo.define('pos_interface_change.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { patch } = require('web.utils');

    let PaymentScreenCustom = PaymentScreen =>
        class extends PaymentScreen {
            async _finalizeValidation() {
                if(this.env.pos.config.x_pos_display_stock){
                    this.sub_qty();
                }
                super._finalizeValidation();
            }

            sub_qty() {
                var self = this;
                var order = this.env.pos.get_order()
                var orderlines = order.get_orderlines();
                var sub_qty_by_product_id = {};
                var ids = [];
                orderlines.forEach(function (line) {
                    if (!sub_qty_by_product_id[line.product.id]) {
                        sub_qty_by_product_id[line.product.id] = line.quantity;
                        ids.push(line.product.id);
                    } else {
                        sub_qty_by_product_id[line.product.id] += line.quantity;
                    }
                });

                console.log('Demo');
                console.log(self);

                ids.forEach(function (id) {
                    if (self.env.pos.db.product_by_id[id] !== false && self.env.pos.db.product_by_id[id] !== undefined) {
                        if(self.env.pos.db.product_by_id[id].type != 'service'){
                            var available = self.env.pos.db.product_by_id[id].available - sub_qty_by_product_id[id];
                            self.env.pos.db.product_by_id[id].on_hand = available;
                            self.env.pos.db.product_by_id[id].incoming_qty = available;
                            self.env.pos.db.product_by_id[id].outgoing_qty = available;
                            self.env.pos.db.product_by_id[id].qty_available = available;
                            self.env.pos.db.product_by_id[id].available = available;
                        }
                    }
                });
            }
        }

    Registries.Component.extend(PaymentScreen, PaymentScreenCustom);

    return PaymentScreen;
});