odoo.define('l10n_hn_edi_pos.pos', function (require) {
    "use strict";

    var { PosGlobalState, Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosHnEdiGlobalState = (PosGlobalState) =>
        class PosHnEdiGlobalState extends PosGlobalState {
            _loadPoSConfig() {
                super._loadPoSConfig(...arguments);
                this.db.save('nextNumber', this.config.number_next_actual);
                this.db.save('indexRefund', this.config.number_next_actual_refund);
            }

            newTicket(){
               let nextNumber = this.db.load('nextNumber');
               nextNumber++;
               this.db.save('nextNumber', nextNumber);
               if (!this.env.pos.config.is_refunded) {
                    this.env.pos.config.l10_hn_number_receipt = this.calculateSequenceNumber(this.env.pos.config.l10_hn_number_receipt);
               } else {
                 this.env.pos.config.l10n_hn_edi_number_receipt_refund = this.calculateSequenceNumber(this.env.pos.config.l10n_hn_edi_number_receipt_refund);
                 let index_refunded = this.db.load('indexRefund')
                 index_refunded++;
                 this.db.save('indexRefund', index_refunded);

               }
            }

            areThereMoreTickets(){
                this.env.pos.config.l10n_hn_edi_sag = "";
                this.env.pos.config.l10n_hn_edi_diplomatic = "";
                this.env.pos.config.l10_hn_exempt_purchase = "";
                this.env.pos.config.l10n_hn_exempted_proof = "";
                const { l10n_hn_final_fiscal_correlative: final_fiscal, l10n_hn_edi_authorization_end_date: end_date} = this.env.pos.config;
                let nextNumber = this.db.load('nextNumber');
                return !(nextNumber > final_fiscal || moment(new Date()).format('YYYY-MM-DD') > end_date);
            }

            areThereMoreTicketsRefund(){
                let indexRefund = Number(this.env.pos.db.load('indexRefund')) + 1;
                let lastTicketRefund = this.env.pos.config.l10n_hn_final_fiscal_correlative_refund;
                let configEndDateRefund = this.env.pos.config.end_date_refund;
                return !(moment(new Date()).format('YYYY-MM-DD') > configEndDateRefund || indexRefund > lastTicketRefund);
            }


            calculateSequenceNumber(number_receipt_incremented){
                let number_receipt = number_receipt_incremented;
                let increment = parseInt(number_receipt.split("-").pop()) + 1;
                let sequence_increment = "00000000".substring(increment.toString().length, 8) + increment;
                let number_receipt_increment = number_receipt.slice(0, -8);
                return number_receipt_increment + sequence_increment;
            }

            async getDocumentNumberRefund() {
                return await this.env.services.rpc({
                    model: 'pos.config',
                    method: 'get_next_document_number',
                    args: [this.config.id],
                });
            }

        }
    Registries.Model.extend(PosGlobalState, PosHnEdiGlobalState);

    const PosHnEdiOrder = (Order) => class PosHnEdiOrder extends Order {

        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json['l10n_hn_edi_sag'] = this.l10n_hn_edi_sag;
            json['l10n_hn_edi_diplomatic'] = this.l10n_hn_edi_diplomatic;
            json['l10_hn_exempt_purchase'] = this.l10_hn_exempt_purchase;
            json['l10n_hn_exempted_proof'] = this.l10n_hn_exempted_proof;
            json['l10n_hn_edi_number_receipt_refund'] = this.l10n_hn_edi_number_receipt_refund;
            return json;
//            return {
//                ...super.export_for_printing(...arguments),
//                l10n_hn_edi_sag: this.l10n_hn_edi_sag,
//                l10n_hn_edi_diplomatic: this.l10n_hn_edi_diplomatic,
//                l10_hn_exempt_purchase: this.l10_hn_exempt_purchase,
//                l10n_hn_exempted_proof: this.l10n_hn_exempted_proof,
//                l10n_hn_edi_number_receipt_refund: this.l10n_hn_edi_number_receipt_refund,
//            };
        }

        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.l10n_hn_edi_sag = json.l10n_hn_edi_sag;
            this.l10n_hn_edi_diplomatic = json.l10n_hn_edi_diplomatic;
            this.l10_hn_exempt_purchase = json.l10_hn_exempt_purchase;
            this.l10n_hn_exempted_proof = json.l10n_hn_exempted_proof;
            this.l10n_hn_edi_number_receipt_refund = json.l10n_hn_edi_number_receipt_refund;
        }


    }
    Registries.Model.extend(Order, PosHnEdiOrder);

});