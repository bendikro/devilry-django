Ext.define('devilry_examiner.controller.DashboardController', {
    extend: 'Ext.app.Controller'

    views: [
        #'dashboard.Dashboard'
        'dashboard.YourAssignments'
    ]

    stores: ['YourAssignments']

    refs: [{
        ref: 'yourAssignments'
        selector: 'yourAssignments'
    }],

    init: () ->
        this.control({
            'yourAssignments': {
                render: this._onRenderYourAssignments
            }
        })

    _onRenderYourAssignments: ->
        @getYourAssignmentsStore().load({
            scope: this
            callback: (assignmentRecords, operation) ->
                if operation.success
                    for assignment in assignmentRecords
                        console.log assignment.get('long_name')
                    @getYourAssignments().update({
                        assignments: assignmentRecords
                    })
                else
                    console.error "ERROR", operation
        })
})
