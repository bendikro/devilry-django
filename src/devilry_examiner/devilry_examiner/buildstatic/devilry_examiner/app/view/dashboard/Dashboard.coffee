Ext.define('devilry_examiner.view.dashboard.Dashboard', {
    extend: 'Ext.container.Container'
    alias: 'widget.dashboard'
    cls: 'devilry_dashboard'

    layout: 'fit'
    padding: '40'
    autoScroll: true

    items: [{
        xtype: 'box'
        html: 'Hello world'
    }]
})
