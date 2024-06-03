odoo.define('l10n_hn_edi_pos.PaymentScreen', function(require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const { useState } = owl;

    const PosHnEdiPaymentScreen = PaymentScreen => class extends PaymentScreen {

        setup() {
            super.setup();
            this.state = useState({
                sag: "",
                diplomatic: "",
                exempt_purchase: "",
                exempted_proof: ""
            });
        }
        async validateOrder(isForceValidate) {
            this.env.pos.newTicket();
            await super.validateOrder(...arguments);
        }

        changeSag(event){
            this.state.sag = event.target.value;
            this.env.pos.config.l10n_hn_edi_sag = this.state.sag;
//            const order = this.env.pos.get_order();
//            if (!order) return;
            this.currentOrder.l10n_hn_edi_sag = this.env.pos.config.l10n_hn_edi_sag;
        }

        changeDiplomatic(event){
            this.state.diplomatic = event.target.value;
            this.env.pos.config.l10n_hn_edi_diplomatic = this.state.diplomatic;
//            const order = this.env.pos.get_order();
//            if (!order) return;
            this.currentOrder.l10n_hn_edi_diplomatic = this.env.pos.config.l10n_hn_edi_diplomatic;
        }

        changeExemptPurchase(event){
            this.state.exempt_purchase = event.target.value;
            this.env.pos.config.l10_hn_exempt_purchase = this.state.exempt_purchase;
//            const order = this.env.pos.get_order();
//            if (!order) return;
            this.currentOrder.l10_hn_exempt_purchase = this.env.pos.config.l10_hn_exempt_purchase;
        }

        changeExemptedProof(event){
            this.state.exempted_proof = event.target.value;
            this.env.pos.config.l10n_hn_exempted_proof = this.state.exempted_proof;
//            const order = this.env.pos.get_order();
//            if (!order) return;
            this.currentOrder.l10n_hn_exempted_proof = this.env.pos.config.l10n_hn_exempted_proof;
        }

        async _isOrderValid(isForceValidate) {
            if ( !this.currentOrder.get_partner() ) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t("Seleccione un cliente"),
                    body: this.env._t("Para continuar debe seleccionar un cliente."),
                });
                return false;
            }
            return super._isOrderValid(isForceValidate);
        }

    };
    Registries.Component.extend(PaymentScreen, PosHnEdiPaymentScreen);
    return PosHnEdiPaymentScreen;
});