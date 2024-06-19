odoo.define('bi_pos_package_pricelist.model', function (require) {
        "use strict";

        const Registries = require('point_of_sale.Registries');
        var core = require('web.core');
        var _t = core._t;
        var {PosGlobalState, Order, Product, Orderline} = require('point_of_sale.models');
        const {Gui} = require('point_of_sale.Gui');

        const PackageProductPosGlobalState = (PosGlobalState) => class PackageProductPosGlobalState extends PosGlobalState {

            async _processData(loadedData) {
                await super._processData(...arguments);

                var product = await this.env.services.rpc({
                    model: 'product.product',
                    method: 'search_read',
                    fields: ['id', 'name', 'packaging_ids'],
                });
                this.pro = []
                for (var i = 0; i < product.length; i++) {
                    if (product[i].packaging_ids) {
                        if (product[i].packaging_ids.length > 0) {
                            this.pro.push(product[i].id)
                        }
                    }
                }
                var products_package = await this.env.services.rpc({
                    model: 'product.packaging',
                    method: 'search_read',
                    fields: [],
                });
                this.products_package = products_package;

                this.products_package = loadedData['product.packaging'];
                await this._loadProductPackage();

            }

            _loadProductPackage(){
                this.products_package_by_id = {}
                for (let pp of this.products_package) {
                    this.products_package_by_id[pp.id] = pp;
                }
            }
        }
        Registries.Model.extend(PosGlobalState, PackageProductPosGlobalState);

        const OrderPackageProduct = (Order) => class OrderPackageProduct extends Order {
            constructor() {
                super(...arguments);
                this.current_package = this.current_package || false;
            }
            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                json.current_package = this.current_package;
                return json;
            }

            export_for_printing() {
                const json = super.export_for_printing(...arguments);
                json.current_package = this.current_package;
                return json;
            }

            init_from_JSON(json) {
                super.init_from_JSON(...arguments);
                this.current_package = json.current_package;
            }
        }
        Registries.Model.extend(Order, OrderPackageProduct);


        const ProductPackage = (Product) => class ProductPackage extends Product {
            get_price(pricelist, quantity, price_extra) {
                var self = this;
                var date = moment();

                // In case of nested pricelists, it is necessary that all pricelists are made available in
                // the POS. Display a basic alert to the user in this case.
                if (pricelist === undefined) {
                    alert(_t(
                        'An error occurred when loading product prices. ' +
                        'Make sure all pricelists are available in the POS.'
                    ));
                }

                var pricelist_items = _.filter(
                    self.applicablePricelistItems[pricelist.id],
                    function (item) {
                        return self.isPricelistItemUsable(item, date);
                    }
                );

                var price = self.lst_price;
                if (price_extra) {
                    price += price_extra;
                }
                if (self.packaging_ids.length > 0 && quantity > 1) {
                    pricelist_items = _.filter(pricelist_items, function (item) {
                        if(item.product_package_id){
                            return (item.applied_on == "4_package") && (item.product_package_id[0] == self.id);
                        }
                    });
                    _.find(pricelist_items, function (rule) {
                        if(rule.package_id){
                            let pp = self.pos.products_package_by_id[rule.package_id[0]];

                            if (pp && pp.qty == quantity) {
                                if (rule.min_quantity && quantity < rule.min_quantity) {
                                    return false;
                                }
                                if (rule.base === 'pricelist') {
                                    price = self.get_price(rule.base_pricelist, quantity);
                                } else if (rule.base === 'standard_price') {
                                    price = self.standard_price;
                                }

                                if (rule.compute_price === 'fixed') {
                                    price = rule.fixed_price;
                                    return true;
                                } else if (rule.compute_price === 'percentage') {
                                    price = price - (price * (rule.percent_price / 100));
                                    return true;
                                } else {
                                    var price_limit = price;
                                    price = price - (price * (rule.price_discount / 100));
                                    if (rule.price_round) {
                                        price = round_pr(price, rule.price_round);
                                    }
                                    if (rule.price_surcharge) {
                                        price += rule.price_surcharge;
                                    }
                                    if (rule.price_min_margin) {
                                        price = Math.max(price, price_limit + rule.price_min_margin);
                                    }
                                    if (rule.price_max_margin) {
                                        price = Math.min(price, price_limit + rule.price_max_margin);
                                    }
                                    return true;
                                }
                            }                            
                        }

                        return false;
                    });
                } else {
                    _.find(pricelist_items, function (rule) {
                        if (rule.min_quantity && quantity < rule.min_quantity) {
                            return false;
                        }
                        if (rule.base === 'pricelist') {
                            price = self.get_price(rule.base_pricelist, quantity);
                        } else if (rule.base === 'standard_price') {
                            price = self.standard_price;
                        }

                        if (rule.compute_price === 'fixed') {
                            price = rule.fixed_price;
                            return true;
                        } else if (rule.compute_price === 'percentage') {
                            price = price - (price * (rule.percent_price / 100));
                            return true;
                        } else {
                            var price_limit = price;
                            price = price - (price * (rule.price_discount / 100));
                            if (rule.price_round) {
                                price = round_pr(price, rule.price_round);
                            }
                            if (rule.price_surcharge) {
                                price += rule.price_surcharge;
                            }
                            if (rule.price_min_margin) {
                                price = Math.max(price, price_limit + rule.price_min_margin);
                            }
                            if (rule.price_max_margin) {
                                price = Math.min(price, price_limit + rule.price_max_margin);
                            }
                            return true;
                        }

                        return false;
                    });
                }

                return price;
            }
        }
        Registries.Model.extend(Product, ProductPackage);

        const PosOrderLine = (Orderline) => class PosOrderLine extends Orderline {

            constructor() {
                super(...arguments);
                this.is_pack_line = this.is_pack_line || false;
                this.pack = this.pack || false;
                this.current = this.current || false;
            }

            show_product_package() {
                var self = this
                var orderline = this
                Gui.showPopup("Packagepopup", {
                    'title': _t('Add Package Product'),
                    'orderlines': orderline.props.line.pack,
                    'orderline': orderline.props.line,
                    confirm: function () {
                        var order = self.env.pos.get_order();
                        var product = order.selected_orderline.product;
                        var set_pack = false;
                        if (orderline.props.line.current.id == orderline.props.line.order.selected_or_package) {
                            set_pack = orderline.props.line.current;
                        } else {
                            for (var i = 0; i < orderline.props.line.pack.length; i++) {
                                if (orderline.props.line.pack[i].id == orderline.props.line.order.selected_or_package) {
                                    set_pack = orderline.props.line.pack[i]
                                    orderline.props.line.current = orderline.props.line.pack[i]
                                }
                            }

                        }
                        orderline.props.line.set_pack_vals(set_pack)
                        var qtyVals = order.pack_prices
                        orderline.props.line.set_pack_price(qtyVals)

                        if (set_pack) {
                            orderline.props.line.selected_pac = set_pack.id
                            var qtyVals = (set_pack.package_price)
                            var qTyVals = qtyVals.toFixed(2)
                            orderline.props.line.set_pack_price(qTyVals)
                        }
                        this.env.posbus.trigger('close-popup', {
                            popupId: this.props.id,
                            response: {confirmed: true},
                        });
                        return
                    }
                });

            }

            get_pack_name() {
                return this.is_pack_line;
            }

            get_pack_quantity() {
                return this.set_pack_quanity;
            }

            export_for_printing() {
                const json = super.export_for_printing(...arguments);
                json.is_pack_line = this.get_pack_name();
                json.receipt_quantity = this.get_pack_quantity();
                return json;
            }

            set_pack_vals(set_pack) {
                var order = this.pos.get_order()
                this.set_pack = set_pack
                if (set_pack) {
                    if (set_pack.id != this.product.id) {
                        this.is_pack_line = set_pack.display_name
                    } else {
                        this.is_pack_line = false
                    }
                    this.set_quantity((this.set_pack.qty) * order.productQty)
                    this.set_pack_quanity = ((this.get_quantity()) / set_pack.qty)
                    this.set_unit_price(set_pack.package_price/set_pack.qty)
                    if (this.get_quantity() == 0) {
                        order.remove_orderline(this);
                    }
                }
                // this.trigger('change',this);
            }


            set_pack_price(qtyVals) {
                this.pack_price = qtyVals
                // this.trigger('change', this);
            }

            set_pack_list(pack) {
                this.pack = pack
                // this.trigger('change',this);
            }

            get_pack_vals(is_pack_line) {
                return this.is_pack_line;
            }

            get_pack() {
                return this.pack
            }

            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                json.set_pack = this.set_pack
                json.pack = this.pack
                json.current_pack = this.current_pack
                json.is_pack_line = this.is_pack_line;
                json.pack_price = this.pack_price;
                json.current = this.current
                json.set_pack_quanity = this.set_pack_quanity;

                return json;
            }
            init_from_JSON(json) {
                super.init_from_JSON(...arguments);
                this.pack = json.pack
                this.current_pack = json.current_pack
                this.is_pack_line = json.is_pack_line
                this.current = json.current
                this.pack_price = json.pack_price
                this.set_pack_quanity = json.set_pack_quanity
            }
        }
        Registries.Model.extend(Orderline, PosOrderLine);

    }
);