odoo.define('pos_interface_change.models', function (require) {
    "use strict";

    let models = require('point_of_sale.models');

//    models.load_fields("pos.config", ['x_display_product_list','x_display_order_list','x_background_color','x_logo',
//        'x_position_categories','x_toggle_numpad','x_position_button','']);
//
//    models.load_fields('product.product', ['type','virtual_available',
//		'qty_available','incoming_qty','outgoing_qty','quant_text']);
//
//    models.load_models({
//		model: 'stock.location',
//		fields: ['id','name'],
//		loaded: function(self, locations){
//			self.locations = locations[0];
//			if (self.config.show_stock_location == 'specific')
//			{
//				for(let i = 0; i < locations.length; i++){
//					if(locations[i].id === self.config.stock_location_id[0]){
//						self.locations =  locations[i];
//					}
//				}
//			}
//		},
//	});

    return models;
});