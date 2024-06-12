odoo.define('pos_interface_change.ProductsWidget', function(require) {
    'use strict';

    const ProductsWidget = require('point_of_sale.ProductsWidget');
    const Registries = require('point_of_sale.Registries');

    let ProductsWidgetCustom = ProductsWidget =>
        class extends ProductsWidget {

            mounted() {
                super.mounted();
				this.env.pos.on('change:is_sync', this.render, this);
				let self = this;
				self.env.services.bus_service.updateOption('pos.sync.stock',self.env.session.uid);
				self.env.services.bus_service.onNotification(self,self._onProductNotification);
				self.env.services.bus_service.startPolling();
				self.env.services.bus_service._startElection();
            }

            _onProductNotification(notifications){
				let self = this;
				_.each(notifications,function(not){
					let prod_data = JSON.parse(not.type.prod_data);
					let prod_id = JSON.parse(not.type.id);
					let product = self.env.pos.db.get_product_by_id(prod_id);
					product.pos = self.env.pos;
					if(self.env.pos.db.product_by_id[product.id]){
						$.each(prod_data, function( key, val ){
							if(key == 'qty_available'){
								product['qty_available'] = val;
								product['on_hand'] = val;
							}
							else if(key == 'virtual_available'){
								product['virtual_available'] = val;
							}
							else if(key == 'incoming_qty'){
								product['incoming_qty'] = val;
							}
							else if(key == 'outgoing_qty'){
								product['outgoing_qty'] = val;
							}
							else if (key == 'quant_text') {
								let data = JSON.parse(val)
								$.each(data, function( i, j ){
									product['quant_text'] = val;
								})
							}
						})
						self.env.pos.db.product_by_id[product.id] = new models.Product({}, product);
					}

				})
				let call = self.productsToDisplay;
				this.env.pos.set("is_sync",true);
			}

			willUnmount() {
				super.willUnmount();
				this.env.pos.off('change:is_sync', null, this);
			}

			get is_sync() {
				return this.env.pos.get('is_sync');
			}

			get productsToDisplay() {
				let self = this;
				let prods = super.productsToDisplay;
				let location = this.env.pos.config.x_stock_location_id;
				if (self.env.pos.config.x_show_stock_location == 'specific'){
					if (self.env.pos.config.x_pos_stock_type == 'onhand'){
						$.each(prods, function( i, prd ){
							prd['on_hand'] = 0;
                            prd['virtual_available'] = 0;
							let loc_onhand = JSON.parse(prd.quant_text);
							$.each(loc_onhand, function( k, v ){
								if(location[0] == k){
									prd['on_hand'] = v[0];
								}
							})
						});
					}
					if (self.env.pos.config.x_pos_stock_type == 'available'){

						$.each(prods, function( i, prd ){
							let loc_available = JSON.parse(prd.quant_text);
							prd['available'] = 0;
							prd['virtual_available'] = 0;
							let total = 0;
							let out = 0;
							let inc = 0;
							$.each(loc_available, function( k, v ){
								if(location[0] == k){
									total += v[0];
									if(v[1]){
										out += v[1];
									}
									if(v[2]){
										inc += v[2];
									}
									let final_data = (total + inc) - out
									prd['available'] = final_data;
									prd['virtual_available'] = final_data;
								}
							})
						});
					}
				}
				else{
					$.each(prods, function( i, prd ){
						prd['on_hand'] = prd.qty_available;
						prd['available'] = prd.virtual_available;
					});
				}
				return prods
			}


            get category_position() {
                return this.env.pos.config.x_position_categories;
            }

            get show_product_list() {
                return this.env.pos.config.x_display_product_list;
            }

            get background(){
                return this.env.pos.config.x_background_color;
            }
        };

    Registries.Component.extend(ProductsWidget, ProductsWidgetCustom);

    return ProductsWidget;



});