from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field, HTML

from devilry.apps.core.models import Assignment
from devilry_examiner.views.add_deadline import DevilryDatetimeFormField



class AssignmentAddStudentsView(UpdateView):
    model = Assignment
    template_name = 'devilry_subjectadmin/assignment_add_students_form.django.html'
    pk_url_kwarg = 'id'
    context_object_name = 'assignment'

    def get_success_url(self):
        return reverse('devilry_subjectadmin_assignment', kwargs=self.kwargs)

    def get_queryset(self):
        return Assignment.where_is_admin_or_superadmin(self.request.user)

    def get_form_class(self):
        class AssignmentAddStudentsForm(forms.ModelForm):
            first_deadline = DevilryDatetimeFormField(
                label=_('First deadline'),
                help_text=_('TODO. Format: "YYYY-MM-DD hh:mm".'),
            )

            class Meta:
                model = Assignment
                fields = ['first_deadline']

            def __init__(self, *args, **kwargs):
                super(AssignmentAddStudentsForm, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.layout = Layout(
                    'first_deadline',
                    HTML('<hr>'),
                    ButtonHolder(
                        Submit('submit', _('Add students'), css_class='btn-lg')
                    )
                )
        return AssignmentAddStudentsForm