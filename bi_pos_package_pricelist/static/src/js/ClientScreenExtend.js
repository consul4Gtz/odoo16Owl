odoo.define('bi_pos_package_pricelist.ClientScreenExtend', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const ClientScreen = require('point_of_sale.ClientListScreen'); 
	const NumberBuffer = require('point_of_sale.NumberBuffer');

	const deleteOrderline = (ClientScreen) =>
		class extends ClientScreen {
			constructor() {
				super(...arguments);
			}
			get nextButton() {
				if(this.env.pos.config.remove_orderline){    
					this.env.pos.bind('change:selectedClient', function() {
						var order = this.env.pos.get_order()
						var orderlines = order.get_orderlines()
						if(orderlines.length > 0){
							for (var line in orderlines)
							{
								if(orderlines[line] && orderlines[line].is_pack_line){
									order.remove_orderline(orderlines[line]);
								}
							}
						}
					});
				}
				if (!this.props.client) {
					return { command: 'set', text: 'Set Customer' };
				} else if (this.props.client && this.props.client === this.state.selectedClient) {
					return { command: 'deselect', text: 'Deselect Customer' };
				} else {
					return { command: 'set', text: 'Change Customer' };
				}
			}
			
			
			
			
			
		};

	Registries.Component.extend(ClientScreen, deleteOrderline);

	return ClientScreen;

});