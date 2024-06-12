odoo.define('pos_interface_change.Chrome', function(require) {
    'use strict';

    const Chrome = require('point_of_sale.Chrome');
    const Registries = require('point_of_sale.Registries');

    let ChromeScreen = Chrome =>
        class extends Chrome {
            get background(){
                if (typeof this.env.pos == "undefined"){
                    return '#865a7b';
                }
                if (this.env.pos.config != null){
                    return this.env.pos.config.x_background_color;
                } else {
                    return '#865a7b';
                }
            }

            get logo(){
                if (typeof this.env.pos == "undefined"){
                    return false;
                }
                if (this.env.pos.config != null){
                    if(this.env.pos.config.x_logo == false){
                        return false;
                    }
                    const config = this.env.pos.config;
                    return `/web/image?model=pos.config&field=x_logo&id=${config.id}&write_date=${config.write_date}&unique=1`;
                } else {
                    return false;
                }
            }
        };

    Registries.Component.extend(Chrome, ChromeScreen);

    return Chrome;


});