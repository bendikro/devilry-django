from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

from .views.feedbackeditor import SchemaFeedbackEditorView
#from .views.feedbackeditor import SchemaFeedbackBulkEditorView


urlpatterns = patterns('devilry_gradingsystemplugin_points',
    url('^feedbackeditor/(?P<deliveryid>\d+)$', SchemaFeedbackEditorView.as_view(),
        name='devilry_gradingsystemplugin_form_feedbackeditor'),
    # url('^feedbackbulkeditor/(?P<assignmentid>\d+)$', SchemaFeedbackBulkEditorView.as_view(),
        # name='devilry_gradingsystemplugin_form_feedbackbulkeditor'),
)
