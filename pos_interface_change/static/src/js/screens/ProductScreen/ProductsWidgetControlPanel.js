odoo.define('pos_interface_change.ProductsWidgetControlPanel', function(require) {
    'use strict';

    const ProductsWidgetControlPanel = require('point_of_sale.ProductsWidgetControlPanel');
    const Registries = require('point_of_sale.Registries');

    let ProductsWidgetControlPanelCustom = ProductsWidgetControlPanel =>
        class extends ProductsWidgetControlPanel {
            get background(){
                if (typeof this.env.pos == "undefined"){
                    return '#865a7b';
                }
                if (this.env.pos.config != null){
                    return this.env.pos.config.x_background_color;
                } else {
                    return '#865a7b';
                }
            }
        };

    Registries.Component.extend(ProductsWidgetControlPanel, ProductsWidgetControlPanelCustom);

    return ProductsWidgetControlPanel;

});