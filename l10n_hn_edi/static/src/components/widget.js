/** @odoo-module **/

import { Component, useState } from '@odoo/owl';
import { registry } from "@web/core/registry";
import { xml } from '@odoo/owl/tags';
//import { Component } from "@odoo/owl";

class MyOwlWidget extends Component {
    static template = xml`
        <div>
            <span t-esc="props.value"/>
        </div>
    `;
    
    setup() {
        this.state = useState({
            value: this.props.value,
        });
    }
}

registry.category("fields").add('my_owl_widget', MyOwlWidget);