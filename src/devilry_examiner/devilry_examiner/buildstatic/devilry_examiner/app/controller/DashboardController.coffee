Ext.define('devilry_examiner.controller.DashboardController', {
    extend: 'Ext.app.Controller'

    views: [
        'dashboard.Dashboard'
    ]

    stores: []

    init: () ->
        this.control({
            'viewport dashboard': {
                render: this._onRender
            }
        })

    _onRender: ->
        console.log 'Render'

    ###
    _onLoadSuccess: function(records) {
        this.getAllWhereIsAdminList().update({
            loadingtext: null,
            list: this._flattenListOfActive(records)
        })
    }
    ###
})
