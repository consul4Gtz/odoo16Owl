odoo.define('bi_pos_package_pricelist.pos_db', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	var PosDB = require('point_of_sale.DB');


	PosDB.include({
		add_packagings: function(productPackagings){
	        productPackagings.forEach(productPackaging => {
	            if (productPackaging.product_id[0] in this.product_by_id) {
	                this.product_packaging_by_barcode[productPackaging.barcode] = productPackaging;
	                this.product_packaging_by_barcode[productPackaging.barcode_2] = productPackaging;
	                this.product_packaging_by_barcode[productPackaging.barcode_3] = productPackaging;
	                this.product_packaging_by_barcode[productPackaging.barcode_4] = productPackaging;
	            }
	        });
	    },
		
	});


});
