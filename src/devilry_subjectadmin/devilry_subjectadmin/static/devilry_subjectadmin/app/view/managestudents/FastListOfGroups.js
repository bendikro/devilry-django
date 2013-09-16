/**
 * List of groups.
 */
Ext.define('devilry_subjectadmin.view.managestudents.FastListOfGroups' ,{
    extend: 'devilry_extjsextras.CheckboxList',
    alias: 'widget.fastlistofgroups',
    cls: 'devilry_subjectadmin_fastlistofgroups',
    bodyCls: 'bootstrap',
    store: 'Groups',

    requires: [
        'devilry_subjectadmin.view.managestudents.DynamicLoadMenu',
        'devilry_subjectadmin.view.managestudents.SelectGroupsBySearchWidget',
        'devilry_subjectadmin.view.managestudents.SelectedGroupsButton',
        'devilry_subjectadmin.view.managestudents.SortByButton'
    ],

    itemTpl: [
        '<div class="groupInfoWrapper groupInfoWrapper_{id}" style="white-space:normal !important;">',
            '<div class="name"><strong>',
                '<tpl if="groupUrlPrefix">',
                    '<a href="{groupUrlPrefix}{id}">',
                        '{fullnames}',
                    '</a>',
                '<tpl else>',
                    '{fullnames}',
                '</tpl>',
            '</strong></div>',
            '<tpl if="groupname">',
                '<div class="groupname">{groupname}</div>',
            '</tpl>',
            '<div class="username"><small class="muted">{usernames}</small></div>',
            '<div class="status">',
                '<div class="status-{status}">',
                    '<tpl if="status === \'corrected\'">',
                        '<tpl if="feedback.is_passing_grade">',
                            '<div class="passinggrade">',
                                '<small class="passingstatus text-success">{approvedText}</small>',
                                ' <small class="grade text-success">({feedback.grade})</small>',
                            '</div>',
                        '</tpl>',
                        '<tpl if="!feedback.is_passing_grade">',
                            '<div class="notpassinggrade">',
                            '<small class="passingstatus text-warning">{notApprovedText}</small>',
                            ' <small class="grade text-warning">({feedback.grade})</small>',
                            '</div>',
                        '</tpl>',
                    '<tpl elseif="status === \'waiting-for-deliveries\'">',
                        '<em><small class="muted">', gettext('Waiting for deliveries'), '</small></em>',
                    '<tpl elseif="status === \'waiting-for-feedback\'">',
                        '<em><small class="muted">', gettext('Waiting for feedback'), '</small></em>',
                    '<tpl else>',
                        '<span class="label label-important">{status}</span>',
                    '</tpl>',
                '</div>',
            '</div>',
        '</div>'
    ],


    prepareItemData: function(record) {
        var groupname = record.get('name');
        if(!Ext.isEmpty(groupname)) {
            groupname = Ext.String.ellipsis(groupname, 20);
        }
        var data = {
            fullnames: this.getFullnames(record),
            groupname: groupname,
            usernames: this.getUsernames(record),
            notApprovedText: this.notApprovedText,
            approvedText: this.approvedText,
            groupUrlPrefix: this.groupUrlPrefix
        };
        Ext.apply(data, record.data);
        return data;
    },

    getFullnames: function(record) {
        var candidates = record.get('candidates');
        if(candidates.length === 0) {
            return Ext.String.format('{0}(groupID={1})', gettext('No-students'), record.get('id'));
        }
        var names = [];
        for(var index=0; index<candidates.length; index++)  {
            var candidate = candidates[index];
            var full_name = candidate.user.full_name;
            if(Ext.isEmpty(full_name)) {
                full_name = Ext.String.format('{0}(userID={1})',
                    gettext('Missing-fullname'), candidate.user.id);
            }
            names.push(full_name);
        }
        return names.join('<br/>');
    },

    /**
     * Get the text for the username DIV.
     *
     * Prioritized in this order:
     * 1. If no candidates, return empty string.
     * 2. Comma-separated list of usernames.
     * */
    getUsernames: function(record) {
        var candidates = record.get('candidates');
        if(candidates.length === 0) {
            return '';
        }
        var usernames = [];
        for(var index=0; index<candidates.length; index++)  {
            var candidate = candidates[index];
            usernames.push(candidate.user.username);
        }
        return usernames.join(', ');
    },

    initComponent: function() {
        Ext.apply(this, {
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'top',
                items: [{
                    xtype: 'selectgroupsbysearch',
                    grid: this,
                    flex: 1
                }]
            }, {
                xtype: 'toolbar',
                dock: 'top',
                items: [{
                    xtype: 'button',
                    text: gettext('Select'),
                    cls: 'selectButton',
                    menu: {
                        xtype: 'menu',
                        cls: 'selectMenu',
                        items: [{
                            itemId: 'selectall',
                            cls: 'selectAllButton',
                            text: gettext('Select all') + ' <small>(CTRL-a)</small>'
                        }, {
                            itemId: 'deselectall',
                            cls: 'deselectAllButton',
                            text: gettext('Deselect all')
                        }, {
                            itemId: 'invertselection',
                            cls: 'invertSelectionButton',
                            text: gettext('Invert selection')
                        }, '-', {
                            text: gettext('Replace current selection'),
                            cls: 'replaceSelectionButton',
                            itemId: 'replaceSelectionButton',
                            hideOnClick: false,
                            menu: this._createSelectMenu({
                                itemId: 'replaceSelectionMenu',
                                cls: 'replaceSelectionMenu',
                                title: gettext('Replace current selection')
                            })
                        }, {
                            itemId: 'addToSelectionButton',
                            cls: 'addToSelectionButton',
                            text: gettext('Add to current selection'),
                            hideOnClick: false,
                            menu: this._createSelectMenu({
                                title: gettext('Add to current selection'),
                                itemId: 'addToSelectionMenu'
                            })
                        }]
                    }
                }, {
                    xtype: 'sortgroupsbybutton',
                    grid: this
                //}, '->', {
                    //xtype: 'selectedgroupsbutton',
                    //grid: this
                }]
            }, {
                xtype: 'toolbar',
                //ui: 'footer',
                dock: 'bottom',
                defaults: {
                    scale: 'large'
                },
                items: ['->', {
                    xtype: 'button',
                    scale: 'medium',
                    itemId: 'addstudents',
                    cls: 'addstudents',
                    text: [
                        '<i class="icon-plus"></i> ',
                        gettext('Add students')
                    ].join('')
                }]
            }]
        });
        this.callParent(arguments);
    },


    /**
     * @param {String} [config.title] Title of the menu
     * @param {[Object]} [config.prefixItems] Prefixed to the items in the menu, under the title.
     */
    _createSelectMenu: function(config) {
        var menuitems = [Ext.String.format('<b>{0}:</b>', config.title)];
        if(config.prefixItems) {
            Ext.Array.push(menuitems, config.prefixItems);
        }
        Ext.Array.push(menuitems, [{

        // Status
            text: pgettext('group', 'By status'),
            cls: 'byStatusButton',
            hideOnClick: false,
            menu: {
                xtype: 'menu',
                cls: 'byStatusMenu',
                items: [{
                    itemId: 'selectStatusOpen',
                    cls: 'selectStatusOpen',
                    text: pgettext('group', 'Open')
                }, {
                    itemId: 'selectStatusClosed',
                    cls: 'selectStatusClosed',
                    text: pgettext('group', 'Closed')
                }]
            }

        // Feedback
        }, {
            text: pgettext('group', 'By feedback'),
            cls: 'byFeedbackButton',
            hideOnClick: false,
            menu: {
                xtype: 'menu',
                cls: 'byFeedbackMenu',
                items: [{
                    itemId: 'selectGradePassed',
                    cls: 'selectGradePassed',
                    text: pgettext('group', 'Passed')
                }, {
                    itemId: 'selectGradeFailed',
                    cls: 'selectGradeFailed',
                    text: pgettext('group', 'Failed')
                }, '-', {
                    itemId: 'selectHasFeedback',
                    cls: 'selectHasFeedback',
                    text: pgettext('group', 'Has feedback')
                }, {
                    itemId: 'selectNoFeedback',
                    cls: 'selectNoFeedback',
                    text: pgettext('group', 'No feedback')
                }, '-', {
                    text: pgettext('group', 'Grade'),
                    cls: 'selectByFeedbackWithGrade',
                    hideOnClick: false,
                    menu: {
                        xtype: 'dynamicloadmenu',
                        itemId: 'specificGradeMenu'
                    }
                }, {
                    text: pgettext('points', 'Points'),
                    cls: 'selectByFeedbackWithPoints',
                    hideOnClick: false,
                    menu: {
                        xtype: 'dynamicloadmenu',
                        itemId: 'specificPointsMenu'
                    }
                }]
            }

        // Number of deliveries
        }, {
            text: gettext('By number of deliveries'),
            cls: 'byDeliveryNumButton',
            hideOnClick: false,
            menu: {
                xtype: 'menu',
                cls: 'byDeliveryMenu',
                items: [{
                    itemId: 'selectHasDeliveries',
                    cls: 'selectHasDeliveries',
                    text: gettext('Has deliveries')
                }, {
                    itemId: 'selectNoDeliveries',
                    cls: 'selectNoDeliveries',
                    text: gettext('No deliveries')
                }, {
                    text: pgettext('numdeliveries', 'Exact number'),
                    cls: 'selectByDeliveryExactNum',
                    hideOnClick: false,
                    menu: {
                        xtype: 'dynamicloadmenu',
                        itemId: 'specificNumDeliveriesMenu'
                    }
                }]
            }

        // By examiner
        }, {
            text: gettext('By examiner'),
            cls: 'byExaminerButton',
            hideOnClick: false,
            menu: {
                xtype: 'menu',
                cls: 'byExaminerMenu',
                items: [{
                    itemId: 'selectHasExaminer',
                    cls: 'selectHasExaminer',
                    text: gettext('Has examiner(s)')
                }, {
                    itemId: 'selectNoExaminer',
                    cls: 'selectNoExaminer',
                    text: gettext('No examiner(s)')
                }, {
                    text: gettext('Specific examiner'),
                    cls: 'selectBySpecificExaminer',
                    hideOnClick: false,
                    menu: {
                        xtype: 'dynamicloadmenu',
                        itemId: 'specificExaminerMenu'
                    }
                }]
            }

        // By tag
        }, {
            text: gettext('By tag'),
            cls: 'byTagButton',
            hideOnClick: false,
            menu: {
                xtype: 'menu',
                cls: 'byTagMenu',
                items: [{
                    itemId: 'selectHasTag',
                    cls: 'selectHasTag',
                    text: gettext('Has tag(s)')
                }, {
                    itemId: 'selectNoTag',
                    cls: 'selectNoTag',
                    text: gettext('No tag(s)')
                }, {
                    text: gettext('Specific tag'),
                    cls: 'selectBySpecificTac',
                    hideOnClick: false,
                    menu: {
                        xtype: 'dynamicloadmenu',
                        itemId: 'specificTagMenu'
                    }
                }]
            }
        }]);
        var menu = {
            xtype: 'menu',
            plain: true,
            itemId: config.itemId,
            cls: config.cls,
            items: menuitems
        };
        return menu;
    }
});
