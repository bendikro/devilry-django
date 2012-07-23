/**
 * Plugin for {@link devilry_subjectadmin.controller.managestudents.Overview} that
 * adds the ability to add students (groups with a single student) to an
 * assignment.
 */
Ext.define('devilry_subjectadmin.controller.managestudents.AddStudentsPlugin', {
    extend: 'Ext.app.Controller',

    views: [
        'managestudents.AddStudentsPanel',
    ],

    mixins: ['devilry_subjectadmin.utils.LoadAssignmentMixin'],

    models: [
        'Assignment'
    ],
    stores: [
        'RelatedStudentsRo',
        'RelatedExaminersRo',
        'Groups'
    ],

    requires: [
        'Ext.tip.ToolTip'
    ],

    refs: [{
        ref: 'addStudentsPanel',
        selector: 'addstudentspanel'
    }, {
        ref: 'selectedStudentsGrid',
        selector: 'addstudentspanel grid'
    }, {
        ref: 'automapExaminersCheckbox',
        selector: 'addstudentspanel #automapExaminersCheckbox'
    }, {
        ref: 'includeTagsCheckbox',
        selector: 'addstudentspanel #includeTagsCheckbox'
    }, {
        ref: 'tagsColumn',
        selector: 'addstudentspanel #tagsColumn'
    }, {
        ref: 'tagsAndExaminersColumn',
        selector: 'addstudentspanel #tagsAndExaminersColumn'
    }],

    init: function() {
        this.control({
            //'viewport managestudentsoverview button[itemId=addstudents]': {
                //click: this._onAddstudents
            //},
            'addstudentspanel': {
                render: this._onRender
            },

            'addstudentspanel #saveButton': {
                click: this._onSave
            },
            'addstudentspanel #allowDuplicatesCheckbox': {
                change: this._onAllowDuplicatesChange,
                render: this._setTooltip
            },
            'addstudentspanel #includeTagsCheckbox': {
                change: this._onIncludeTagsChange,
                render: this._setTooltip
            },
            'addstudentspanel #automapExaminersCheckbox': {
                change: this._onAutomapExaminersChange,
                render: this._setTooltip
            }
        });
    },

    _setTooltip: function(item) {
        var tip = Ext.create('Ext.tip.ToolTip', {
            target: item.el,
            constrainPosition: true,
            anchor: 'top',
            dismissDelay: 30000, // NOTE: Setting this high (30sec) instead of to 0 (no autodismiss) so that it disappears eventually even when the framework do not catch the event that should hide it.
            html: item.tooltip
        });
    },

    _onRender: function() {
        var assignment_id = this.getAddStudentsPanel().assignment_id;
        this.loadAssignment(assignment_id);
    },

    onLoadAssignmentSuccess: function(record) {
        console.log(record);
        this.assignmentRecord = record;
        var period_id = this.assignmentRecord.get('parentnode');

        this.getRelatedExaminersRoStore().setPeriod(period_id);
        this.getRelatedStudentsRoStore().setPeriod(period_id);

        var relatedStudentsStore = this.getRelatedStudentsRoStore();
        relatedStudentsStore.loadWithAutomaticErrorHandling({
            scope: this,
            success: this._onLoadRelatedStudentsStoreSuccess,
            errortitle: gettext('Failed to load students from the period')
        });
    },

    _handleLoadError: function(operation, title) {
        var error = Ext.create('devilry_extjsextras.DjangoRestframeworkProxyErrorHandler', operation);
        error.addErrors(null, operation);
        var errormessage = error.asHtmlList();
        Ext.widget('htmlerrordialog', {
            title: title,
            bodyHtml: errormessage
        }).show();
    },
    onLoadAssignmentFailure: function(operation) {
        this.getOverview().setLoading(false);
        this._handleLoadError(operation, gettext('Failed to load assignment'));
    },

    _onLoadRelatedStudentsStoreSuccess: function(records) {
        var relatedExaminersStore = this.getRelatedExaminersRoStore();
        relatedExaminersStore.loadWithAutomaticErrorHandling({
            scope: this,
            success: this._onLoad,
            errortitle: gettext('Failed to load examiners from the period')
        });
    },

    _onLoad: function() {
        this.relatedExaminersMappedByTag = this.getRelatedExaminersRoStore().getMappedByTags();
        var relatedStudentsStore = this.getRelatedStudentsRoStore();
        relatedStudentsStore.clearFilter();

        this._filterOutRelatedStudentsAlreadyInGroup();
        relatedStudentsStore.sortBySpecialSorter('full_name');

        console.log('LOADED');
        //this.manageStudentsController.setBody({
            //xtype: 'addstudentspanel',
            //relatedStudentsStore: relatedStudentsStore,
            //periodinfo: this.manageStudentsController.getPeriodInfo(),
            //relatedExaminersMappedByTag: this.relatedExaminersMappedByTag
        //});
        this._setBody();
    },

    _filterOutRelatedStudentsAlreadyInGroup: function() {
        var relatedStudentsStore = this.getRelatedStudentsRoStore();
        var currentUsers = this.getGroupsStore().getGroupsMappedByUserId();
        relatedStudentsStore.filterBy(function(relatedStudentRecord) {
            var userid = relatedStudentRecord.get('user').id;
            return typeof currentUsers[userid] == 'undefined';
        });
    },

    _onAllowDuplicatesChange: function(field, allowDuplicates) {
        if(allowDuplicates) {
            this.getRelatedStudentsRoStore().clearFilter();
        } else {
            this._filterOutRelatedStudentsAlreadyInGroup();
        }
        this._setBody();
    },
    _onIncludeTagsChange: function(field, includeTags) {
        if(includeTags) {
            this.getTagsColumn().show();
            this.getAutomapExaminersCheckbox().enable();
        } else {
            if(this.getAutomapExaminersCheckbox().getValue() == true) {
                this.getAutomapExaminersCheckbox().setValue(false);
                // NOTE: we do nothing more because changing automapExaminersCheckbox will trigger _onAutomapExaminersChange
            } else {
                this.getTagsColumn().hide();
            }
            this.getAutomapExaminersCheckbox().disable();
        }
    },
    _onAutomapExaminersChange: function(field, automapExaminers) {
        if(automapExaminers) {
            this.getTagsColumn().hide();
            this.getTagsAndExaminersColumn().show();
        } else {
            //this.getTagsColumn().show();
            this.getTagsAndExaminersColumn().hide();
            if(this.getIncludeTagsCheckbox().getValue() == true) {
                this.getTagsColumn().show();
            }
        }
    },

    _onSave: function(button) {
        var selModel = this.getSelectedStudentsGrid().getSelectionModel();
        var selectedRelatedStudents = selModel.getSelection();
        var groupsStore = this.getGroupsStore();
        var includeTags = this.getIncludeTagsCheckbox().getValue();
        var automapExaminers = this.getAutomapExaminersCheckbox().getValue();

        Ext.Array.each(selectedRelatedStudents, function(relatedStudentRecord) {
            var groupRecord = groupsStore.addFromRelatedStudentRecord({
                relatedStudentRecord: relatedStudentRecord,
                includeTags: includeTags
            });
            if(automapExaminers) {
                groupRecord.setExaminersFromMapOfRelatedExaminers(this.relatedExaminersMappedByTag);
            }
        }, this);
        //this.manageStudentsController.notifyMultipleGroupsChange();
    },


    _setBody: function() {
        var ignoredcount = this.getRelatedStudentsRoStore().getTotalCount() - this.getRelatedStudentsRoStore().getCount()
        var allIgnored = this.getRelatedStudentsRoStore().getTotalCount() == ignoredcount;
        this.getAddStudentsPanel().setBody({
            ignoredcount: ignoredcount,
            allIgnored: allIgnored,
            relatedExaminersMappedByTag: this.relatedExaminersMappedByTag,
            periodinfo: {
                path: 'TOOD',
                id: 1000
            }
        });
    }
});
