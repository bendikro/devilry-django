Ext.define('devilry_extjsextras.ScriptTagTemplateComponent', {
    extend: 'Ext.Component',

    constructor: function(config) {
        if(Ext.isEmpty(config)) {
            config = {};
        }
        element = Ext.get(this.renderTo);
        scriptTag = Ext.get(this.tplId);
        config.tpl = scriptTag.dom.innerText;
        this.callParent([config]);
    }
});
