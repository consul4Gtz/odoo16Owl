odoo.define('q_pos_ticket.models', require => {
    "use strict";

    let models = require('point_of_sale.models');
    const orderline_super = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({
        export_for_printing: function () {
            var res = orderline_super.export_for_printing.apply(this, arguments);
            res.product_default_code = this.get_product().default_code;
            return res;
        },
    });
});