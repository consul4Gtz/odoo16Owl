/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePopover } from "@web/core/popover/popover_hook";

const { Component, EventBus, onWillRender } = owl;

export class widPopover extends Component {
}
//ShowWarehouseSaleLineStockProduct
//ProductWarehouseSaleLineStockPopOver -> DetailPopOver
widPopover.template = "sale_stock_by_warehouse.DetailPopOver";

export class StockWidget extends Component {
    setup() {
        this.bus = new EventBus();
        this.popover = usePopover();
        this.closePopover = null;
        this.initCalcData();
    }

    initCalcData() {
        // calculate data not in record
        const { data } = this.props.record;
        var info = JSON.parse(data.sale_line_stock_widget);
        if (!info) {
         console.log('No hay datos')
         return;
        }
        return info;
    }
    
    //funcion para mostrar el popover y cargar los datos en la plantilla, se llama desde el template con el evento click
    // para invocar los datos el objeto definido en el constructor del popover se llama: ejemplo props.title en la plantilla
    showPopup(ev) {
        //this.updateCalcData();
        const $content = this.initCalcData();
        //console.log($content);
        //console.log($content.title);
        if(!$content){
            return;
        }else{
        this.closePopover = this.popover.add(
            ev.currentTarget,
            this.constructor.components.Popover,
            {bus: this.bus, 
                lines: $content,
                title: $content.title, },
            {
                position: 'top',
            }
            );

        this.bus.addEventListener('close-popover', this.closePopover);
    }
    }
}

StockWidget.components = { Popover: widPopover  };
StockWidget.template = "sale_stock_by_warehouse.ShowWarehouseSaleLineStockProducts";
StockWidget.supportedTypes = ["char"];

registry.category("fields").add("sale_line_stock_widget_js", StockWidget);

//registry.category("view_widgets").add("sale_line_stock_widget_js", StockWidget);
//"fields"
