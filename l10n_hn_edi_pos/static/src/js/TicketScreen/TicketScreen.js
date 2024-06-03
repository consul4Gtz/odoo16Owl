odoo.define('l10n_hn_edi_pos.TicketScreen', function(require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');

    const PosHnEdiTicketScreen = TicketScreen =>
        class extends TicketScreen {
            async _onDoRefund() {
                if (!this.env.pos.areThereMoreTicketsRefund()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('No Tickets'),
                        body: this.env._t('No more sales tickets are available.'),
                    });
                    return;
                }
                this.env.pos.getDocumentNumberRefund();
                this.env.pos.config.is_refunded = true;
                const order = this.getSelectedSyncedOrder();

                if (!order) {
                    this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                    this.render();
                    return;
                }

                if (this._doesOrderHaveSoleItem(order)) {
                    this._prepareAutoRefundOnOrder(order);
                }

                const partner = order.get_partner();

                const allToRefundDetails = Object.values(this.env.pos.toRefundLines).filter(
                    ({ qty, orderline, destinationOrderUid }) =>
                        !this.env.pos.isProductQtyZero(qty) &&
                        (partner ? orderline.orderPartnerId == partner.id : true) &&
                        !destinationOrderUid
                );
                if (allToRefundDetails.length == 0) {
                    this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                    this.render();
                    return;
                }

                const destinationOrder =
                    this.props.destinationOrder && partner === this.props.destinationOrder.get_partner()
                        ? this.props.destinationOrder
                        : this.env.pos.add_new_order({ silent: true });

                for (const refundDetail of allToRefundDetails) {
                    const { qty, orderline } = refundDetail;
                    await destinationOrder.add_product(this.env.pos.db.get_product_by_id(orderline.productId), {
                        quantity: -qty,
                        price: orderline.price,
                        lst_price: orderline.price,
                        extras: { price_manually_set: true },
                        merge: false,
                        refunded_orderline_id: orderline.id,
                        tax_ids: orderline.tax_ids,
                        discount: orderline.discount,
                    });
                    refundDetail.destinationOrderUid = destinationOrder.uid;
                }

                if (partner && !destinationOrder.get_partner()) {
                    destinationOrder.set_partner(partner);
                }
                destinationOrder.l10n_hn_edi_number_receipt_refund = this.env.pos.calculateSequenceNumber(this.env.pos.config.l10n_hn_edi_number_receipt_refund);
                this._onCloseScreen();
                return destinationOrder;
            }
        }
    Registries.Component.extend(TicketScreen, PosHnEdiTicketScreen);
    return PosHnEdiTicketScreen;
});