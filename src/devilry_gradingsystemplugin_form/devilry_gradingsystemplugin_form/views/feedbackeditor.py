from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Field

from devilry_gradingsystem.views.feedbackeditorbase import FeedbackEditorFormBase
from devilry_gradingsystem.views.feedbackeditorbase import FeedbackEditorFormView
from devilry_gradingsystem.views.feedbackbulkeditorbase import FeedbackBulkEditorFormBase
from devilry_gradingsystem.views.feedbackbulkeditorbase import FeedbackBulkEditorFormView
from devilry_gradingsystem.models import FeedbackDraft
from devilry_examiner.views.bulkviewbase import BulkViewBase


class SchemaFeedbackEditorForm(FeedbackEditorFormBase):
    points = forms.IntegerField(
        label=_('Points'))

    def __init__(self, *args, **kwargs):
        super(SchemaFeedbackEditorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('points')
        )
        self.add_common_layout_elements()


class SchemaFeedbackEditorView(FeedbackEditorFormView):
    template_name = 'devilry_gradingsystemplugin_form/feedbackeditor.django.html'
    form_class = SchemaFeedbackEditorForm

    def get_initial_from_last_draft(self):
        initial = super(SchemaFeedbackEditorView, self).get_initial_from_last_draft()
        initial['points'] = self.last_draft.points
        return initial

    def get_points_from_form(self, form):
        return form.cleaned_data['points']


"""
class SchemaFeedbackBulkEditorForm(FeedbackBulkEditorFormBase):
    points = forms.IntegerField(
        label=_('Points'))

    def __init__(self, *args, **kwargs):
        super(SchemaFeedbackBulkEditorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('points')
        )
        self.add_common_layout_elements()

class SchemaFeedbackBulkEditorView(FeedbackBulkEditorFormView):
    template_name = 'devilry_gradingsystemplugin_form/feedbackbulkeditor.django.html'
    form_class = SchemaFeedbackBulkEditorForm

    def get_initial_from_draft(self, draft):
        initial = super(SchemaFeedbackBulkEditorView, self).get_initial_from_draft(draft)
        initial['points'] = draft.points
        return initial

    def get_default_points_value(self):
        return ''

    def get_points_from_form(self, form):
        return form.cleaned_data['points']

"""
