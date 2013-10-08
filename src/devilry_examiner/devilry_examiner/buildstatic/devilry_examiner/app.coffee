Ext.application({
    name: 'devilry_examiner'
    appFolder: DevilrySettings.DEVILRY_STATIC_URL + '/devilry_examiner/app'
    paths: {
        'devilry_extjsextras': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_extjsextras'
        #'devilry_theme': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_theme'
        'devilry_i18n': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_i18n'
        'devilry_header': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_header/app'
        'devilry_authenticateduserinfo': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_authenticateduserinfo'
    }

    requires: [
        'Ext.container.Viewport'
        'Ext.layout.container.Border'
        'Ext.layout.container.Column'
        'Ext.layout.container.Card'
        'devilry_extjsextras.Router'
        'devilry_extjsextras.RouteNotFound'
        'devilry_extjsextras.AlertMessage'
        'devilry_header.Header'
        'devilry_header.Breadcrumbs'
        'devilry_extjsextras.FloatingAlertmessageList'
        'devilry_authenticateduserinfo.UserInfo'
    ]

    controllers: [
        'DashboardController'
    ]

    refs: [{
        ref: 'alertmessagelist'
        selector: 'viewport floatingalertmessagelist#appAlertmessagelist'
    }]

    constructor: ->
        this.callParent(arguments)

    launch: ->
        this._createViewport()

    _createViewport: ->
        this.viewport = Ext.create('Ext.container.Viewport', {
            xtype: 'container'
            layout: 'border'
        })
        this.viewport.setLoading()
        devilry_authenticateduserinfo.UserInfo.load(this._onUserInfoLoaded, this)

    _onUserInfoLoaded: (userInfoRecord) ->
        this.userInfoRecord = userInfoRecord
        this.breadcrumbs = Ext.create('devilry_header.Breadcrumbs')
        this.primaryContentContainer = Ext.widget('container', {
            region: 'center'
            layout: 'fit'
        })
        this.viewport.removeAll()
        this.viewport.add([{
            xtype: 'devilryheader'
            region: 'north'
            navclass: 'examiner'
            breadcrumbs: this.breadcrumbs
        }, {
            xtype: 'container'
            region: 'center'
            cls: 'devilry_subtlebg'
            layout: 'fit'
            items: [{
                xtype: 'floatingalertmessagelist'
                itemId: 'appAlertmessagelist'
                anchor: '100%'
            }, this.primaryContentContainer]
        }])
        this.viewport.setLoading(false)
        this._onViewportReady()

    _onViewportReady: ->
        this._setupRoutes()

    setPrimaryContent: (component) ->
        this.primaryContentContainer.removeAll()
        this.primaryContentContainer.add(component)

    ###
    Called after something has been deleted.
    @param short_description A short description of the item that was deleted.
    ###
    onAfterDelete: (short_description) ->
        this.route.navigate('')


    ###
    Used by controllers to set the page title (the title-tag).
    ###
    setTitle: (title) ->
        window.document.title = Ext.String.format('{0} - Devilry', title)


    ###
    Routing
    ###

    _setupRoutes: ->
        this.route = Ext.create('devilry_extjsextras.Router', this, {
            listeners: {
                scope: this
                beforeroute: this._beforeRoute
            }
        })
        this.route.add("", 'dashboard')
        this.route.start()

    _beforeRoute: (route, routeInfo) ->
        this.getAlertmessagelist().removeAll()

    routeNotFound: (routeInfo) ->
        this.breadcrumbs.set([], gettext('Route not found'))
        this.setPrimaryContent({
            xtype: 'routenotfound'
            route: routeInfo.token
        })

    dashboard: ->
        this.breadcrumbs.setHome()
        this.setPrimaryContent({
            xtype: 'dashboard'
        })
})
