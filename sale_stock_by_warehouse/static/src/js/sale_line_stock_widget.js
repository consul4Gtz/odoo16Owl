odoo.define('sale_stock_by_warehouse.SaleLineStockWidget', function (require) {
"use strict";

var core = require('web.core');


var Widget = require('web.Widget');
var widget_registry = require('web.widget_registry');
//var utils = require('web.utils');
var QWeb = core.qweb;
var _t = core._t;

//var ShowStockLineWidget = AbstractField.extend({
var SaleLineShowStockLineWidget = Widget.extend({
    template: 'sale_stock_by_warehouse.ShowWarehouseSaleLineStockProduct',
    events: _.extend({}, Widget.prototype.events, {  'click .fa-area-chart': '_onClickButton', }),

    init: function (parent, params) {
        this.data = params.data;
        this.fields = params.fields;
        //this._updateData();
        this._super(parent);
    },

    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self._setPopOver();
        });
    },

    updateState: function (state) {
        this.$el.popover('dispose');
        var candidate = state.data[this.getParent().currentRow];
        if (candidate) {
            this.data = candidate.data;
            //this._updateData();
            this.renderElement();
            this._setPopOver();
        }
    },

    _getContent() {
        var info = JSON.parse(this.data.sale_line_stock_widget);
        //console.log('DATA2: '+ info.content)
        if (!info) {
            return;
        }
        const $content = $(QWeb.render('sale_stock_by_warehouse.ProductWarehouseSaleLineStockPopOver', {
            lines: info,
        }));

        //$content.on('click', '.action_open_forecast', this._openForecast.bind(this));
        return $content;
    },

    _setPopOver() {
        const $content = this._getContent();
        if (!$content) {
            return;
        }
        const options = {
            content: $content,
            html: true,
            placement: 'left',
            title: _t('Availability'),
            //title: $content.title,
            trigger: 'focus',
            delay: {'show': 0, 'hide': 100 },
        };
        this.$el.popover(options);
    },

    _onClickButton: function () {
        // We add the property special click on the widget link.
        // This hack allows us to trigger the popover (see _setPopOver) without
        // triggering the _onRowClicked that opens the order line form view.
        this.$el.find('.fa-area-chart').prop('special_click', true);
    },
});



//field_registry.add('stock', ShowStockLineWidget)
widget_registry.add('sale_line_stock_widget', SaleLineShowStockLineWidget);
return SaleLineShowStockLineWidget;
})
