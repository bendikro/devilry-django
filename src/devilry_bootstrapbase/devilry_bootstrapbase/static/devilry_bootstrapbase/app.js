Ext.application({
    name: 'devilry_bootstrapbase',
    appFolder: DevilrySettings.DEVILRY_STATIC_URL + '/devilry_bootstrapbase/app',
    paths: {
        'devilry_extjsextras': DevilrySettings.DEVILRY_STATIC_URL + '/devilry_extjsextras'
    },

    requires: [
        'devilry_extjsextras.Router',
        'devilry_extjsextras.RouteNotFound'
    ],

    controllers: [],

    launch: function() {
        this._setupRoutes();
    },

    /** Used by controllers to set the page title (the title-tag). */
    setTitle: function(title) {
        window.document.title = Ext.String.format('{0} - Devilry', title);
    },


    /*********************************************
     * Routing
     ********************************************/

    _setupRoutes: function() {
        this.route = Ext.create('devilry_extjsextras.Router', this, {
            includePhysicalPath: true
        });
        this.route.add("/example", 'dashboard');
        this.route.add("/example#testroute", 'testroute');
        this.route.start();
    },
    
    routeNotFound: function(routeInfo) {
        console.error('Route not found:', routeInfo.token);
    },

    dashboard: function() {
        console.log('dashboard route triggered');
    },
    testroute: function() {
        console.log('testroute triggered');
    }
});
