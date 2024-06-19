odoo.define('bi_pos_package_pricelist.Packagepopup', function (require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    var {Orderline} = require('point_of_sale.models');
    const { onMounted } = owl;
    class Packagepopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            onMounted(this._mounted);
        }

        _mounted() {
            var options = this.props
            var order = this.env.pos.get_order()
            if (options.confirm) {
                if (order.selected_or_package) {
                    if (options.orderline) {
                        order.selected_or_package = options.orderline.current.id
                    }
                }
                $('.PackVals').css('visibility', 'visible');
                var select_pack_vals = options.orderlines[options.orderline.selected_pac]
                var list1 = []
                for (var t = 0; t < options.orderlines.length; t++) {
                    if (options.orderlines[t].id == options.orderline.current.id) {
                        list1.push(options.orderlines[t])
                    }
                }
                $("#" + options.orderline.current.id).css("background-color", "#afc8f1")

                var set_price = this.env.pos.format_currency((options.orderline.price * options.orderline.quantity))
                $('#packageValue').text(set_price)
                var set_qty = (options.orderline.quantity) / list1[0].qty
                $('#qtyVals').val(set_qty)


            } else {
                $('.PackVals').css('visibility', 'hidden');
            }
        }

        click_confirm(event) {
            var self = this
            let product;
            if (this.props.orderlines.length > 1){
                product = this.env.pos.db.get_product_by_id(this.props.orderlines[1].product_id[0])
            }else{
                
                if (this.props.orderlines[0].product_id){
                    product = this.env.pos.db.get_product_by_id(this.props.orderlines[0].product_id[0])
                }else{
                    product = this.env.pos.db.get_product_by_id(this.props.orderlines[0].id)
                }
            }
            var order = this.env.pos.get_order()
            if (order.current_package) {
                var x = order.current_package.package_price;
                var y = order.current_package.qty;

                var qtyVals = $("#qtyVals").val()

                order.productQty = qtyVals
                var formated = this.env.pos.format_currency((x * qtyVals) * y);
                $('#packageValue').text(formated)

                
                var line = Orderline.create({}, {pos: this.env.pos, order: order, product: product});
                // line.selected = true;
                line.set_selected(true)
                if (this.props.confirm) {
                    this.props.confirm.call(this);
                    self.cancel();
                    return
                }
                var qtyVals = $("#qtyVals").val()
                var to_merge_orderline;
                for (var i = 0; i < order.orderlines.length; i++) {
                    if (order.orderlines[i].selected_pac == order.selected_or_package) {
                        to_merge_orderline = order.orderlines.at(i);
                    }

                }

                if (order.selected_or_package != product.id || to_merge_orderline) {

                    if (to_merge_orderline) {

                        var unit_prire = to_merge_orderline.get_unit_price()
                        var quan = parseInt(to_merge_orderline.get_quantity()) + parseInt(order.current_package.qty * parseInt(qtyVals))
                        to_merge_orderline.set_quantity(quan)
                        to_merge_orderline.set_unit_price(unit_prire)
                        order.select_orderline(to_merge_orderline);
                       this.cancel();
                       return
                    } else {
                        if (order.selected_or_package == product.id) {
                            line.set_quantity(qtyVals)
                            order.orderlines.add(line);
                            order.select_orderline(order.get_last_orderline());

                            this.cancel();
                           return
                        } else {
                            var last_liness = order.orderlines.add(line);
                            order.select_orderline(order.get_last_orderline());
                            var last_orderline = order.get_orderline(line.id);
                            last_orderline.selected_pac = order.selected_or_package
                            // order.add_product(product);
                            if (order){
                                last_orderline.current = order.current_package
                                last_orderline.set_pack_list(order.product_packages)
                                var set_pack = order.current_package
                                if(set_pack){
                                    last_orderline.set_pack_vals(set_pack)

                                    var qtyVals= (set_pack.package_price)
                                    var qTyVals = qtyVals.toFixed(2)
                                    last_orderline.set_pack_price(qTyVals)
                                    this.cancel();
                                }
                            }
                            return true
                        }
                    }
                
                } else {
                    var to_merge
                    for (var i = 0; i < order.orderlines.length; i++) {
                        if (!order.orderlines[i].is_pack_line && order.orderlines[i].product.id == line.product.id) {
                            to_merge = order.orderlines.at(i);
                        }
                    }
                    if (to_merge) {
                        var qty = parseInt(to_merge.get_quantity()) + parseInt(order.current_package.qty * parseInt(qtyVals))
                        to_merge.set_quantity(qty)
                    } else {
                        var qtyVals = $("#qtyVals").val()
                        line.set_quantity(qtyVals)
                        order.orderlines.add(line);
                        order.select_orderline(order.get_last_orderline());

                    }
                    this.cancel()
                }
            }else{
                
                this.cancel()
            }
            return true
        }


        click_on_package_product(event) {
            var product = this.props.selected_product
            var order = this.env.pos.get_order()
            var self = this
            var on_package = parseInt(event.currentTarget.dataset['productId']);
            if ($("#" + on_package)) {
                event.currentTarget[$(".select_package").css("background-color", "white")]
                event.currentTarget[$("#" + on_package).css("background-color", "#afc8f1")]

            }
            
            order.selected_or_package = on_package
            if (!order.product_packages) {
                if (order.get_selected_orderline()){
                    if (order.get_selected_orderline().pack){
                        order.product_packages = order.get_selected_orderline().pack
                        for (var current_order = 0; current_order < order.product_packages.length; current_order++) {
                            if (order.product_packages[current_order].id == on_package) {
                                order.current_package = order.product_packages[current_order]
                                $('.PackVals').css('visibility', 'visible');
                                var x = order.product_packages[current_order].package_price
                                var y = order.product_packages[current_order].qty

                                var qtyVals = $("#qtyVals").val()
                                order.productQty = qtyVals
                                var formated = this.env.pos.format_currency((x * qtyVals));
                                order.pack_prices = formated
                                $('#packageValue').text(formated)

                                $('#qtyVals').focusout(function () {
                                    var formated = self.env.pos.format_currency((x * $("#qtyVals").val()));
                                    order.productQty = $("#qtyVals").val()
                                    $('#packageValue').text(formated)

                                });
                            }
                        }
                    }else{
                        $('.PackVals').css('visibility', 'visible');
                        var x = product.lst_price

                        var qtyVals = $("#qtyVals").val()
                        order.productQty = qtyVals
                        var formated = this.env.pos.format_currency((x * qtyVals));
                        order.pack_prices = formated
                        $('#packageValue').text(formated)

                        $('#qtyVals').focusout(function () {
                            var formated = self.env.pos.format_currency((x * $("#qtyVals").val()));
                            order.productQty = $("#qtyVals").val()
                            $('#packageValue').text(formated)

                        });
                    }
                    
                    
                }else{
                    $('.PackVals').css('visibility', 'visible');
                    var x = product.lst_price

                    var qtyVals = $("#qtyVals").val()
                    order.productQty = qtyVals
                    var formated = this.env.pos.format_currency((x * qtyVals));
                    order.pack_prices = formated
                    $('#packageValue').text(formated)

                    $('#qtyVals').focusout(function () {
                        var formated = self.env.pos.format_currency((x * $("#qtyVals").val()));
                        order.productQty = $("#qtyVals").val()
                        $('#packageValue').text(formated)

                    });

                }
            }else{
                for (var current_order = 0; current_order < order.product_packages.length; current_order++) {
                    if (order.product_packages[current_order].id == on_package) {
                        order.current_package = order.product_packages[current_order]
                        $('.PackVals').css('visibility', 'visible');
                        var x = order.product_packages[current_order].package_price
                        var y = order.product_packages[current_order].qty

                        var qtyVals = $("#qtyVals").val()
                        order.productQty = qtyVals
                        var formated = this.env.pos.format_currency((x * qtyVals));
                        order.pack_prices = formated
                        $('#packageValue').text(formated)

                        $('#qtyVals').focusout(function () {
                            var formated = self.env.pos.format_currency((x * $("#qtyVals").val()));
                            order.productQty = $("#qtyVals").val()
                            $('#packageValue').text(formated)

                        });
                    }
                }
            }
        
        }


    };
    Packagepopup.template = 'Packagepopup';
    Packagepopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: 'Confirm ?',
        orderlines: '',
    };
    Registries.Component.add(Packagepopup);

    return Packagepopup;
});
