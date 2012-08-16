Ext.define('devilry_extjsextras.DatetimeHelpers', {
    singleton: true,

    formatTimedeltaShort: function(delta) {
        if(delta.days > 0) {
            return interpolate(gettext('%s days'), [delta.days]);
        } else if(delta.hours > 0) {
            return interpolate(gettext('%s hours'), [delta.hours]);
        } else if(delta.minutes > 0) {
            return interpolate(gettext('%s minutes'), [delta.minutes]);
        } else {
            return interpolate(gettext('%s seconds'), [delta.seconds]);
        }
    }
});
