Ext.define('devilry_nodeadmin.controller.AggregatedStudentInfoController', {
    extend: 'Ext.app.Controller',

    views: [
        'aggregatedstudentview.AggregatedStudentInfoOverview'
    ],

    refs: [{
        ref: 'AggregatedStudentInfo',
        selector: 'aggregatedstudentinfo'
    }, {
        ref: 'AggregatedStudentInfoBox',
        selector: 'aggregatedstudentinfo #AggregatedStudentInfoBox'
    }],

    models: ['AggregatedStudentInfo'],

    init: function() {
        this.control({
            'viewport aggregatedstudentinfo': {
                render: this._onRender
            }
        });
    },

    _onRender: function() {
        var user_id = this.getAggregatedStudentInfo().user_id;
        this.getAggregatedStudentInfoModel().load(user_id, {
            scope: this,
            callback: function(records, operation) {
                if (operation.success) {
                    this._onLoadSuccess(records);
                } else {
                    this._onLoadFailure();
                }
            }
        });
    },

    _onLoadSuccess: function(record) {
        this.getAggregatedStudentInfoBox().update({data: record.data});
    },

    _onLoadFailure: function(records){
        //TODO
    }
});