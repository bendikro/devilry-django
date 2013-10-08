Ext.define('devilry_examiner.controller.AssignmentController', {
    extend: 'Ext.app.Controller'

    views: [
        'assignment.AssignmentWorkspace'
    ]

    stores: []

    refs: [{
        ref: 'workspace',
        selector: 'viewport assignmentworkspace'
    }]

    init: () ->
        this.control({
            'viewport assignmentworkspace': {
                render: this._onRenderWorkspace
            }
        })

    _onRenderWorkspace: ->
        @assignmentId = @getWorkspace().assignmentId
        console.log 'Render assignment', @assignmentId

    ###
    _onLoadSuccess: function(records) {
        this.getAllWhereIsAdminList().update({
            loadingtext: null,
            list: this._flattenListOfActive(records)
        })
    }
    ###
})
