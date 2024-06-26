odoo.define('pos_interface_change.SyncStock', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');

	class SyncStock extends PosComponent {
		constructor() {
			super(...arguments);
			this.pos_stock_sync();
		}

		pos_stock_sync() {
			var self = this;
			this.env.pos.set('is_sync',true);
		}
	}
	SyncStock.template = 'SyncStock';

	Registries.Component.add(SyncStock);

	return SyncStock;
});