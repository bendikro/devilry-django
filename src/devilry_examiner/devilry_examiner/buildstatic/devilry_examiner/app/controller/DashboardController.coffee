Ext.define('devilry_examiner.controller.DashboardController', {
    extend: 'Ext.app.Controller'

    views: [
        #'dashboard.Dashboard'
        'dashboard.YourAssignments'
    ]

    stores: []

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
        #console.log @getYourAssignments()
        @getYourAssignments().update({
            assignments: [
                {long_name: 'Oblig 1'}
                {long_name: 'Oblig 2'}
            ]
        })
})
