odoo.define('bi_pos_package_pricelist.OrderWidgetExtended', function(require){
	'use strict';

	const OrderWidget = require('point_of_sale.OrderWidget');
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { Component } = owl;

	const OrderSummaryExtended = (OrderWidget) =>
		class extends OrderWidget {
			constructor() {
				super(...arguments);
			}

			async _editPackLotLines(event) {
	            const orderline = event.detail.orderline;
	            const isAllowOnlyOneLot = orderline.product.isAllowOnlyOneLot();
	            const packLotLinesToEdit = orderline.getPackLotLinesToEdit(isAllowOnlyOneLot);
	            const { confirmed, payload } = await this.showPopup('EditListPopup', {
	                title: this.env._t('Lot/Serial Number(s) Required'),
	                isSingleItem: isAllowOnlyOneLot,
	                array: packLotLinesToEdit,
	            });
	            if (confirmed) {
	                // Segregate the old and new packlot lines
	                const modifiedPackLotLines = Object.fromEntries(
	                    payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
	                );
	                const newPackLotLines = payload.newArray
	                    .filter(item => !item.id)
	                    .map(item => ({ lot_name: item.text }));

	                orderline.setPackLotLines({ modifiedPackLotLines, newPackLotLines });
	            }
	            var line = event.detail.orderline
	            var qtyVals= line.set_pack.qty * line.set_pack_quanity
	            line.set_quantity(qtyVals)
	            this.order.select_orderline(event.detail.orderline);
	        }
	};

	Registries.Component.extend(OrderWidget, OrderSummaryExtended);

	return OrderWidget;

});
