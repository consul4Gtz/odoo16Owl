odoo.define('pos_interface_change.TicketScreen', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const TicketScreen = require('point_of_sale.TicketScreen');

    let TicketScreenInherit = TicketScreen =>
        class extends TicketScreen {

            get show_order_list() {
                return this.env.pos.config.x_display_order_list;
            }
            get background(){
                return this.env.pos.config.x_background_color;
            }
            get toggle_numpad() {
                return this.env.pos.config.x_toggle_numpad;
            }

            get button_position() {
                return this.env.pos.config.x_position_button;
            }
        };

    Registries.Component.extend(TicketScreen, TicketScreenInherit);

    return TicketScreen;

});