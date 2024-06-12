odoo.define('pos_interface_change.ProductScreen', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');

    let ProductScreenInherit = ProductScreen =>
        class extends ProductScreen {

            get show_order_list() {
                return this.env.pos.config.x_display_order_list;
            }
            get background(){
                return this.env.pos.config.x_background_color;
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenInherit);

    return ProductScreenInherit;



});