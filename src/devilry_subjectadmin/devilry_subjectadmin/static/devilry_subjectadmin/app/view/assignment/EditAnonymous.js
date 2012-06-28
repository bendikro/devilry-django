/**
 * A window for editing the anonymous attribute of an Assignment.
 * */
Ext.define('devilry_subjectadmin.view.assignment.EditAnonymous', {
    extend: 'Ext.window.Window',
    alias: 'widget.editanonymous',
    cls: 'devilry_subjectadmin_editanonymous bootstrap',
    requires: [
        'devilry_extjsextras.SaveButton'
    ],

    initComponent: function() {
        Ext.apply(this, {
            layout: 'fit',
            width: 460,
            height: 270,
            closable: false,
            modal: true,
            title: gettext('Anonymous'),
            items: {
                xtype: 'form',
                bodyPadding: 20,
                autoScroll: true,
                border: 0,
                layout: 'anchor',
                defaults: {
                    anchor: '100%'
                },
                items: [{
                    xtype: 'alertmessagelist'
                }, {
                    xtype: 'box',
                    tpl: '<p>{help}</p>',
                    data: {
                        help: gettext('For <strong>exams</strong>, this should normally be <em>checked</em>. If an assignment is anonymous, examiners see a candidate-id instead of a username. A candidate-id <strong>must</strong> be set for each student.')
                    },
                    margin: {bottom: 10}
                }, {
                    xtype: 'checkbox',
                    boxLabel: gettext('Anonymous'),
                    name: 'anonymous',
                    uncheckedValue: false,
                    inputValue: true
                }],
                buttons: ['->', {
                    xtype: 'cancelbutton'
                }, {
                    xtype: 'savebutton'
                }]
            }
        });
        this.callParent(arguments);
    }
});
