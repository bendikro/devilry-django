Ext.define('devilry_examiner.model.YourAssignmentsModel', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'results', type: 'auto'},
    ],

    proxy: {
        type: 'ajax',
        # url: DevilrySettings.DEVILRY_URLPATH_PREFIX + '/devilry_nodeadmin/rest/aggregatedstudentinfo/',
        url: 'assignments.json',

        headers: {
            'Accept': 'application/json'
        },

        reader: {
            type: 'json'
        }
    }
})
