odoo.define('bi_pos_package_pricelist.product_package', function (require) {
    "use strict";

    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    let utils = require('web.utils');
    var {Orderline} = require('point_of_sale.models');
    let round_pr = utils.round_precision;
    let core = require('web.core');
    let QWeb = core.qweb;
    let _t = core._t;

    const ProductPackage = (ProductScreen) => class extends ProductScreen {
        constructor() {
            super(...arguments);
        }


        barcode_product_click_confirm(package_product) {
            var self = this
            var order = this.env.pos.get_order()
            let product;
            if (package_product.length > 1){
                product = this.env.pos.db.get_product_by_id(package_product[1].product_id[0])
            }else{
                
                if (package_product[0].product_id){
                    product = this.env.pos.db.get_product_by_id(package_product[0].product_id[0])
                }else{
                    product = this.env.pos.db.get_product_by_id(package_product[0].id)
                }
            }
            var order = this.env.pos.get_order()
            var line = Orderline.create({}, {pos: this.env.pos, order: order, product: product});
            line.set_pack_quanity = 1
            line.set_pack_list(package_product)
            order.productQty = 1
            line.set_pack_vals(package_product[0])
            line.set_pack_price(package_product[0].package_price)
            order.orderlines.add(line);
            order.select_orderline(order.get_last_orderline());
            order.current_package = package_product[0]



            
        }

        async _barcodeProductAction(code) {
            let order = this.env.pos.get_order();
            let product = this.env.pos.db.get_product_by_barcode(code.base_code);
            if (!product) {
                // find the barcode in the backend
                let foundProductIds = [];
                try {
                    foundProductIds = await this.rpc({
                        model: 'product.product',
                        method: 'search',
                        args: [[['barcode', '=', code.base_code]]],
                        context: this.env.session.user_context,
                    });
                } catch (error) {
                    if (isConnectionError(error)) {
                        return this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Network Error'),
                            body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
                        });
                    } else {
                        throw error;
                    }
                }
                if (foundProductIds.length) {
                    await this.env.pos._addProducts(foundProductIds);
                    // assume that the result is unique.
                    product = this.env.pos.db.get_product_by_id(foundProductIds[0]);
                } else {
                    return this._barcodeErrorAction(code);
                }
            }

            if(product.tracking == "none" && product.packaging_ids.length > 0 ){
                let package_product = []
                if (code.base_code == product.barcode){
                    let product_rel_package = this.create_package(product);
                    package_product.push(product_rel_package);
                }
                
                if(this.env.pos.pro.includes(product.id)){
                    
                    if(this.env.pos.config.customer_required){
                        if(order.get_partner()){ 
                            for (let j=0; j<this.env.pos.products_package.length; j++){
                                if (this.env.pos.products_package[j].product_id[0] === product.id){
                                    let eee = this.env.pos.products_package[j]
                                    this.compute_package_price(product,eee)
                                    let is_pack_line = this.env.pos.products_package[j]
                                    if (code.base_code == is_pack_line.barcode || code.base_code == is_pack_line.barcode_2 ||
                                        code.base_code == is_pack_line.barcode_3 || code.base_code == is_pack_line.barcode_4){
                                        package_product.push(is_pack_line)
                                    }
                                    order.product_packages = package_product
                                }
                            }
                            this.barcode_product_click_confirm(package_product);
                            // const options = await this.showPopup('Packagepopup', {
                            //     title: this.env._t('Select Product Pack'),
                            //     orderlines: package_product,
                            //     selected_product:product,
                            // });
                        }
                        else{
                            this.showPopup("ErrorPopup",{
                                'title': "Package Product",
                                'body':"This Product is Package product please select customer First",
                            
                            });
                        }
                    }
                    else{
                        for (let j=0; j<this.env.pos.products_package.length; j++){
                            if (this.env.pos.products_package[j].product_id[0] === product.id){
                                let eee = this.env.pos.products_package[j]
                                this.compute_package_price(product,eee)
                                let is_pack_line = this.env.pos.products_package[j]

                                
                                if (code.base_code == is_pack_line.barcode || code.base_code == is_pack_line.barcode_2 ||
                                    code.base_code == is_pack_line.barcode_3 || code.base_code == is_pack_line.barcode_4){
                                    package_product.push(is_pack_line)
                                }

                                order.product_packages = package_product
                            }
                        }
                        this.barcode_product_click_confirm(package_product);
                        // const options = await this.showPopup('Packagepopup', {
                        //     title: this.env._t('Select Product Pack'),
                        //     orderlines: package_product,
                        //     selected_product:product,
                        // });
                    }
                }
                else{
                    super._barcodeProductAction(code)
                }
                return package_product;
            }else if(product.tracking != "none" && product.packaging_ids.length > 0){
                const { confirmed, payload: selectedOption } = await this.showPopup('SelectionPopup',
                    {
                        title: this.env._t('What do you want to do?'),
                        list: [{id:"0", label: this.env._t("Apply a Lot/Serial Number(s) / Product Configurator "), item: false},
                         {id:"1", label: this.env._t("Add Package Product"), item: true}],
                    });
                if(confirmed){
                    if(!selectedOption){
                        super._barcodeProductAction(code)
                    }else{
                        let package_product = []
                        if (code.base_code == product.barcode){
                            let product_rel_package = this.create_package(product);
                            package_product.push(product_rel_package);
                        }
                        if(this.env.pos.pro.includes(product.id)){
                            
                            if(this.env.pos.config.customer_required){
                                if(order.get_partner()){ 
                                    for (let j=0; j<this.env.pos.products_package.length; j++){
                                        if (this.env.pos.products_package[j].product_id[0] === product.id){
                                            let eee = this.env.pos.products_package[j]
                                            this.compute_package_price(product,eee)
                                            let is_pack_line = this.env.pos.products_package[j]
                                            if (code.base_code == is_pack_line.barcode || code.base_code == is_pack_line.barcode_2 ||
                                        code.base_code == is_pack_line.barcode_3 || code.base_code == is_pack_line.barcode_4){
                                                package_product.push(is_pack_line)
                                            }
                                            order.product_packages = package_product
                                        }
                                    }
                                    this.barcode_product_click_confirm(package_product);
                                    // const options = await this.showPopup('Packagepopup', {
                                    //     title: this.env._t('Select Product Pack'),
                                    //     orderlines: package_product,
                                    //     selected_product:product,
                                    // });
                                }
                                else{
                                    this.showPopup("ErrorPopup",{
                                        'title': "Package Product",
                                        'body':"This Product is Package product please select customer First",
                                    });
                                }
                            }
                            else{
                                for (let j=0; j<this.env.pos.products_package.length; j++){
                                    if (this.env.pos.products_package[j].product_id[0] === product.id){
                                        let eee = this.env.pos.products_package[j]
                                        this.compute_package_price(product,eee)
                                        let is_pack_line = this.env.pos.products_package[j]
                                        if (code.base_code == is_pack_line.barcode || code.base_code == is_pack_line.barcode_2 ||
                                        code.base_code == is_pack_line.barcode_3 || code.base_code == is_pack_line.barcode_4){
                                            package_product.push(is_pack_line)
                                        }
                                        order.product_packages = package_product
                                    }
                                }
                                this.barcode_product_click_confirm(package_product);
                                // const options = await this.showPopup('Packagepopup', {
                                //     title: this.env._t('Select Product Pack'),
                                //     orderlines: package_product,
                                //     selected_product:product,
                                // });
                            }
                        }
                        else{
                            super._barcodeProductAction(code)
                        }
                        return package_product;
                    }
                }                
            }else{
                super._barcodeProductAction(code)
            }
        }

        compute_package_price(product, eee) {
            product.package = "Package"
            eee.package = "Package"
            let self = this
            eee.package_price = product.get_price(
                this.env.pos.get_order().pricelist, eee.qty)
        }
        create_package(product) {
            let order = this.env.pos.get_order();
            let package_price = product.get_price(order.pricelist, 1)
            let pro_pack = {};
            if (product) {
                pro_pack['id'] = product.id;
                pro_pack['name'] = product.display_name;
                pro_pack['display_name'] = product.display_name;
                pro_pack['qty'] = 1
                pro_pack['package_price'] = package_price
                pro_pack['product_uom_id'] = product.uom_id
            }
            return pro_pack
        }

        async _clickProduct(event) {
            let order = this.env.pos.get_order();
            const product = event.detail;

            if(product.tracking == "none" && product.packaging_ids.length > 0 ){
                let package_product = []
                let product_rel_package = this.create_package(product);
                package_product.push(product_rel_package);
                if(this.env.pos.pro.includes(product.id)){
                    
                    if(this.env.pos.config.customer_required){
                        if(order.get_partner()){ 
                            for (let j=0; j<this.env.pos.products_package.length; j++){
                                if (this.env.pos.products_package[j].product_id[0] === product.id){
                                    let eee = this.env.pos.products_package[j]
                                    this.compute_package_price(product,eee)
                                    let is_pack_line = this.env.pos.products_package[j]
                                    for (var item of order.pricelist.items) {
                                        if(item.package_id[0] === eee.id){
                                            package_product.push(eee)
                                            order.product_packages = package_product
                                        }
                                    }
                                }
                            }
                            const options = await this.showPopup('Packagepopup', {
                                title: this.env._t('Select Product Pack'),
                                orderlines: package_product,
                                selected_product:product,
                            });
                        }
                        else{
                            this.showPopup("ErrorPopup",{
                                'title': "Package Product",
                                'body':"This Product is Package product please select customer First",
                            
                            });
                        }
                    }
                    else{
                        for (let j=0; j<this.env.pos.products_package.length; j++){
                            if (this.env.pos.products_package[j].product_id[0] === product.id){
                                let eee = this.env.pos.products_package[j]
                                this.compute_package_price(product,eee)
                                let is_pack_line = this.env.pos.products_package[j]
                                for (var item of order.pricelist.items) {
                                    if(item.package_id[0] === eee.id){
                                        package_product.push(eee)
                                        order.product_packages = package_product
                                    }
                                }
                            }
                        }
                        const options = await this.showPopup('Packagepopup', {
                            title: this.env._t('Select Product Pack'),
                            orderlines: package_product,
                            selected_product:product,
                        });
                    }
                }
                else{
                    super._clickProduct(event)
                }
                return package_product;
            }else if(product.tracking != "none" && product.packaging_ids.length > 0){
                const { confirmed, payload: selectedOption } = await this.showPopup('SelectionPopup',
                    {
                        title: this.env._t('What do you want to do?'),
                        list: [{id:"0", label: this.env._t("Apply a Lot/Serial Number(s) / Product Configurator "), item: false},
                         {id:"1", label: this.env._t("Add Package Product"), item: true}],
                    });
                if(confirmed){
                    if(!selectedOption){
                        super._clickProduct(event)
                    }else{
                        let package_product = []
                        let product_rel_package = this.create_package(product);

                        package_product.push(product_rel_package);
                        if(this.env.pos.pro.includes(product.id)){
                            
                            if(this.env.pos.config.customer_required){
                                if(order.get_partner()){ 
                                    for (let j=0; j<this.env.pos.products_package.length; j++){
                                        if (this.env.pos.products_package[j].product_id[0] === product.id){
                                            let eee = this.env.pos.products_package[j]
                                            this.compute_package_price(product,eee)
                                            let is_pack_line = this.env.pos.products_package[j]
                                            for (var item of order.pricelist.items) {
                                                if(item.package_id[0] === eee.id){
                                                    package_product.push(eee)
                                                    order.product_packages = package_product
                                                }
                                            }
                                        }
                                    }
                                    const options = await this.showPopup('Packagepopup', {
                                        title: this.env._t('Select Product Pack'),
                                        orderlines: package_product,
                                        selected_product:product,
                                    });
                                }
                                else{
                                    this.showPopup("ErrorPopup",{
                                        'title': "Package Product",
                                        'body':"This Product is Package product please select customer First",
                                    
                                    });
                                }
                            }
                            else{
                                for (let j=0; j<this.env.pos.products_package.length; j++){
                                    if (this.env.pos.products_package[j].product_id[0] === product.id){
                                        let eee = this.env.pos.products_package[j]
                                        this.compute_package_price(product,eee)
                                        let is_pack_line = this.env.pos.products_package[j]
                                        for (var item of order.pricelist.items) {
                                            if(item.package_id[0] === eee.id){
                                                package_product.push(eee)
                                                order.product_packages = package_product
                                            }
                                        }
                                    }
                                }
                                const options = await this.showPopup('Packagepopup', {
                                    title: this.env._t('Select Product Pack'),
                                    orderlines: package_product,
                                    selected_product:product,
                                });
                            }
                        }
                        else{
                            super._clickProduct(event)
                        }
                        return package_product;
                    }
                }                
            }else{
                super._clickProduct(event)
            }
        }

        async onClickPartner() {
            // IMPROVEMENT: This code snippet is very similar to selectPartner of PaymentScreen.
            const currentPartner = this.currentOrder.get_partner();
            if (currentPartner && this.currentOrder.getHasRefundLines()) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t("Can't change customer"),
                    body: _.str.sprintf(
                        this.env._t(
                            "This order already has refund lines for %s. We can't change the customer associated to it. Create a new order for the new customer."
                        ),
                        currentPartner.name
                    ),
                });
                return;
            }
            const { confirmed, payload: newPartner } = await this.showTempScreen(
                'PartnerListScreen',
                { partner: currentPartner }
            );
            if (confirmed) {
                this.currentOrder.set_partner(newPartner);
                // this.currentOrder.updatePricelist(newPartner);
            }

            
            
        }

        _setValue(val) {
            let self = this;
            let order = this.currentOrder;
            var orderline = order.get_selected_orderline()
            if (this.currentOrder.get_selected_orderline()) {

                if (this.currentOrder.get_selected_orderline().is_pack_line) {
                    if (this.env.pos.numpadMode === 'quantity') {
                        if (val == 'remove'){
                            order.remove_orderline(orderline)
                        }else{
                            orderline.set_pack_quanity = val
                            var new_qty = val * orderline.order.current_package.qty
                            orderline.set_quantity(new_qty);
                            orderline.set_unit_price(orderline.order.current_package.package_price/orderline.order.current_package.qty);
                        }
                    } else {
                        super._setValue(val)
                    }
                } else {
                    super._setValue(val)
                }
            }

        }
    };

    Registries.Component.extend(ProductScreen, ProductPackage);

    return ProductScreen;

});