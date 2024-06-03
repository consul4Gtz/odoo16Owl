odoo.define('l10n_hn_edi_pos.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

   const PosHnEdiProductScreen = ProductScreen =>
        class extends ProductScreen {
           async _onClickPay() {
                if (this.env.pos.areThereMoreTickets()) {
                    super._onClickPay(...arguments);
                } else {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('No Tickets'),
                        body: this.env._t('No more sales tickets are available.'),
                    });
                }
           }
        }
   Registries.Component.extend(ProductScreen, PosHnEdiProductScreen);
   return PosHnEdiProductScreen;

});