odoo.define('l10n_hn_edi_pos.ReceiptScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const PosHnEdiReceiptScreen = ReceiptScreen =>
        class extends ReceiptScreen {
            orderDone() {
                this.env.pos.config.is_refunded = false;
                return super.orderDone()
            }
        }
    Registries.Component.extend(ReceiptScreen, PosHnEdiReceiptScreen);
    return PosHnEdiReceiptScreen;
});