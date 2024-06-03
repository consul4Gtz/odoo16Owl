odoo.define('l10n_hn_edi_pos.OrderReceipt', function(require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const Registries = require('point_of_sale.Registries');

    const PosHnEdiOrderReceipt = OrderReceipt =>
        class extends OrderReceipt {
            get receiptEnv() {
                let receipt_render_env = super.receiptEnv;
                let receipt = receipt_render_env.receipt;
                receipt.is_refunded = true;
                return receipt_render_env;
            }
            get isRefunded() {
                return this.env.pos.config.is_refunded;
            }
            get configCAI () {
                return this.env.pos.config.l10n_hn_edi_sar_authorization_number || {};
            }
            get configRefundCAI () {
                return this.env.pos.config.l10n_hn_edi_sar_authorization_number || {};
            }
            get receiptNumber () {
                return this.env.pos.config.l10_hn_number_receipt;
            }
            get receiptNumberRefund () {
                return this.env.pos.config.l10n_hn_edi_number_receipt_refund;
            }
            get sag () {
                return this.env.pos.config.l10n_hn_edi_sag;
            }
            get diplomatic () {
                return this.env.pos.config.l10n_hn_edi_diplomatic;
            }
            get exemptPurchase () {
                return this.env.pos.config.l10_hn_exempt_purchase;
            }
            get exemptedProof () {
                return this.env.pos.config.l10n_hn_exempted_proof;
            }

        }
    Registries.Component.extend(OrderReceipt, PosHnEdiOrderReceipt);
    return PosHnEdiOrderReceipt
});