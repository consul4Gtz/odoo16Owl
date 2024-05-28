/** @odoo-module **/

import { Component, useState } from '@odoo/owl';
import { registry } from "@web/core/registry";
//import { xml } from '@odoo/owl/tags';
//import { Component } from "@odoo/owl";

export class MyOwlWidget extends Component {
   
    setup() {
        this.state = useState({
            value: this.props.value,
        });
    }
}
MyOwlWidget .template = "l10n_hn_edi.testfield";
MyOwlWidget .supportedTypes = ["char"];
registry.category("fields").add('my_owl_widget', MyOwlWidget);