Ext.define('devilry_examiner.view.assignment.AssignmentWorkspace', {
    extend: 'Ext.container.Container'
    alias: 'widget.assignmentworkspace'
    cls: 'devilry_assignmentworkspace'

    layout: 'fit'
    padding: '40'
    autoScroll: true

    # Sent in via the route, and read by the controller to load the appropriate assignment.
    assignmentId: null

    items: [{
        xtype: 'box'
        html: 'Assignment workspace'
    }]
})
