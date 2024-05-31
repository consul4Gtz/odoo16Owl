odoo.define('q_pos_ticket.clear_ticket', function(require) {
    'use strict';

    const { PosComponent } = require('point_of_sale.PosComponent');
    const { Registries } = require('point_of_sale.Registries');

    class ClearTicketButton extends PosComponent {
        async onClick() {
            this.env.pos.get_order().destroy(); // This will clear the current order
        }
    }
    ClearTicketButton.template = 'ClearTicketButton';

    Registries.Component.add(ClearTicketButton);
});