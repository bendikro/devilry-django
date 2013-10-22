Ext.define('devilry_examiner.store.YourAssignments', {
    extend: 'Ext.data.Store'
    model: 'devilry_examiner.model.YourAssignment'

    proxy: {
        type: 'rest',
        url: DevilrySettings.DEVILRY_URLPATH_PREFIX + '/devilry_examiner/rest/assignmentlisting/'
        #url: 'assignments.json',

        headers: {
            'Accept': 'application/json'
        },

        reader: {
            type: 'json'
            root: 'items'
        }
    }
})
