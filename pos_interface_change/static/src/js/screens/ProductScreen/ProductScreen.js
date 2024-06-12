odoo.define('pos_interface_change.ProductScreen', function(require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { patch } = require('web.utils');

    let ProductScreenCustom = ProductScreen =>
        class extends ProductScreen {
            get toggle_numpad() {
                return this.env.pos.config.x_toggle_numpad;
            }

            get button_position() {
                return this.env.pos.config.x_position_button;
            }

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

            get show_order_list() {
                return this.env.pos.config.x_display_order_list;
            }

            toogleNumpad() {
                $('.pads').slideToggle(() => {
                    $('.numpad-toggle').toggleClass('fa-caret-down fa-caret-up');
                    if ($(this).is(':visible'))
                        $('.order-scroller').animate({ scrollTop: $('.order-scroller').height() }, 500);
                });
            }



            async _clickProduct(event) {
                let self = this;
				const product = event.detail;
				console.log(self.env.pos.config);
				let allow_order = self.env.pos.config.x_pos_allow_order;
				let deny_order= self.env.pos.config.x_pos_deny_order || 0;
				let call_super = true;
				if(self.env.pos.config.x_pos_display_stock && product.type == 'product'){
					if (allow_order == false){
						if (product.on_hand <= 0 ){
							call_super = false;
							self.showPopup('ErrorPopup', {
								title: self.env._t('Deny Order'),
								body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
							});
						}
					}
//					else{
//						if ( product.on_hand <= deny_order ){
//							call_super = false;
//							self.showPopup('ErrorPopup', {
//								title: self.env._t('Deny Order'),
//								body: self.env._t("Deny Order" + "(" + product.display_name + ")" + " is Out of Stock."),
//							});
//						}
//					}
				}
				if(call_super){
					super._clickProduct(event);
				}
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenCustom);

    return ProductScreen;

});
