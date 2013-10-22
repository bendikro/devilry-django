Ext.application({
    name: 'devilry_examiner'
    appFolder: DevilrySettings.DEVILRY_STATIC_URL + '/devilry_examiner/app'
    paths: {
        'devilry_extjsextras': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_extjsextras'
    }

    requires: [
        'devilry_extjsextras.Router'
        'devilry_extjsextras.RouteNotFound'
    ]

    controllers: [
        'DashboardController'
    ]

    launch: ->
        @_setupRoutes()


    ###
    Used by controllers to set the page title (the title-tag).
    ###
    setTitle: (title) ->
        window.document.title = Ext.String.format('{0} - Devilry', title)


    ###
    Routing
    ###

    _setupRoutes: ->
        @route = Ext.create('devilry_extjsextras.Router', this, {
            includePhysicalPath: true
        })
        @route.add("/", 'dashboard')
        @route.start()

    routeNotFound: (routeInfo) ->
        console.error 'Route not found:', routeInfo.token

    dashboard: ->
        console.log 'dashboard route'
        Ext.create('devilry_examiner.view.dashboard.YourAssignments')

})
