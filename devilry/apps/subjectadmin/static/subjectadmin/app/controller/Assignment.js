/**
 * Controller for the assignment overview.
 */
Ext.define('subjectadmin.controller.Assignment', {
    extend: 'Ext.app.Controller',

    //requires: [
    //],
    views: [
        'assignment.Assignment',
        'ActionList'
    ],

    stores: [
        'SingleAssignment'
    ],

    refs: [{
        ref: 'gradeEditorSidebarBox',
        selector: 'editablesidebarbox[itemId=gradeeditor]'
    }, {
        ref: 'publishingTimeSidebarBox',
        selector: 'editablesidebarbox[itemId=publishingtime]'
    }, {
        ref: 'assignmentView',
        selector: 'assignment'
    }],

    init: function() {
        this.control({
            'viewport assignment editablesidebarbox[itemId=gradeeditor] button': {
                click: this._onEditGradeEditor
            },
            'viewport assignment editablesidebarbox[itemId=publishingtime] button': {
                click: this._onEditPublishingTime
            }
        });
    },

    onLaunch: function() {
        this.subject_shortname = this.getAssignmentView().subject_shortname;
        this.period_shortname = this.getAssignmentView().period_shortname;
        this.assignment_shortname = this.getAssignmentView().assignment_shortname;
        this._loadAssignment();
    },

    _loadAssignment: function() {
        var store = this.getSingleAssignmentStore();
        store.loadAssignment(
            this.subject_shortname, this.period_shortname, this.assignment_shortname,
            this._onLoadAssignment, this
        );
    },

    _onLoadAssignment: function(records, operation) {
        console.log(operation);
        if(operation.success) {
            this._onLoadAssignmentSuccess(records[0]);
        } else {
            this._onLoadAssignmentFailure(operation);
        }
    },

    _onLoadAssignmentFailure: function(operation) {
        var tpl = Ext.create('Ext.XTemplate',
            '<h2>{title}</h2>',
            '<p>{subject_shortname}.{period_shortname}.{assignment_shortname}</p>'
        );
        this.getAssignmentView().getEl().mask(tpl.apply({
            title: dtranslate('themebase.doesnotexist'),
            subject_shortname: this.subject_shortname,
            period_shortname: this.period_shortname,
            assignment_shortname: this.assignment_shortname
        }), 'messagemask');
    },

    _onLoadAssignmentSuccess: function(record) {
        console.log('success', record);
    },

    _onEditGradeEditor: function() {
        console.log('grade', this.getGradeEditorSidebarBox());
    },

    _onEditPublishingTime: function() {
        console.log('pub', this.getPublishingTimeSidebarBox());
    },
});
