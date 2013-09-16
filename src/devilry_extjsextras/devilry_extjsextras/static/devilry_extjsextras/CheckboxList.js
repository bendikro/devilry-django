/**
Button intended as the primary button in a view (the one it is most natural to
click by default).
*/ 
Ext.define('devilry_extjsextras.CheckboxList', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.devilry_checkboxlist',

    requires: [
        'Ext.XTemplate'
    ],

    itemTpl: [
        'item-{id}'
    ],

    /**
     * @cfg {Ext.data.Store} [store]
     * The store to render the list from.
     */

    getStore: function() {
        return Ext.getStore(this.store);
    },
    
    constructor: function(config) {
        this.initConfig(config);
        this.callParent([config]);
        this.itemTplCompiled = Ext.create('Ext.XTemplate', this.itemTpl);
    },

    initComponent: function() {
        this.addCls('devilry_checkboxlist');
        Ext.apply(this, {
            autoScroll: true,
            tpl: [
                '<tpl for="records">',
                    '<div class="devilry_checkboxlist_item">',
                        '<div class="checkboxwrapper"><input type="checkbox"/></div>',
                        '<div class="contentwrapper">{[this.renderItem(values)]}</div>',
                    '</div>',
                '</tpl>', {
                    renderItem: Ext.bind(this._renderItem, this)
                }
            ]
        });
        this.callParent(arguments);
        this.getStore().on('load', this._onLoadStore, this);
        //this.on({
            //scope: this,
            //element: 'el',
            //delegate: '.devilry_checkboxlist_item .checkboxwrapper',
            //click: this._onClickCheckboxWrapper
        //});
    },

    prepareItemData: function(record) {
        return record.data;
    },

    _renderItem: function(record) {
        return this.itemTplCompiled.apply(this.prepareItemData(record));
    },

    _onLoadStore: function(store, records) {
        console.log('Load', records);
        this.update({
            records: records
        });
    },

    selectAll: function() {
        var checkboxes = this.getEl().query('.devilry_checkboxlist_item .checkboxwrapper input', true);
        for(var index=0; index<checkboxes.length; index++)  {
            var checkboxHtmlElement = checkboxes[index];
            this._selectCheckbox(checkboxHtmlElement);
            this._selectItem(this._getItemElement(checkboxHtmlElement));
        }
    },

    _selectCheckbox: function(checkboxHtmlElement) {
        checkboxHtmlElement.checked = true;
    },

    _deSelectCheckbox: function(checkboxHtmlElement) {
        checkboxHtmlElement.checked = false;
    },

    _selectItem: function(itemElement) {
        itemElement.addCls('selected');
    },

    _deSelectItem: function(itemElement) {
        itemElement.removeCls('selected');
    },


    _getItemElement: function(htmlElement) {
        return Ext.get(htmlElement).findParent('.devilry_checkboxlist_item', 50, true);
    },

    _getCheckboxHtmlElement: function(itemElement) {
        return itemElement.down('.checkboxwrapper input', true);
    },

    _onClickCheckboxWrapper: function(e) {
        console.log('_onClickCheckboxWrapper');
        e.preventDefault();
        var itemElement = this._getItemElement(e.element);
        var checkboxHtmlElement = this._getCheckboxHtmlElement(itemElement);
        if(itemElement.hasCls('selected')) {
            this._deSelectItem(itemElement);
            this._deSelectCheckbox(checkboxHtmlElement);
        } else {
            this._selectItem(itemElement);
            this._selectCheckbox(checkboxHtmlElement);
        }
    }
});
