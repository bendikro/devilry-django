# Python imports
from __future__ import unicode_literals

from datetime import datetime
# Django imports
from django import forms
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _, ugettext_lazy, pgettext_lazy

# Devilry/cradmin imports
from django_cradmin import crapp
from django_cradmin.viewhelpers import update, delete
from django_cradmin.crispylayouts import PrimarySubmit, DefaultSubmit
from django_cradmin.acemarkdown.widgets import AceMarkdownWidget
from django_cradmin.widgets.datetimepicker import DateTimePickerWidget
from devilry.devilry_group.views import cradmin_feedbackfeed_base
from devilry.apps.core import models as core_models
from devilry.devilry_group import models as group_models
from devilry.utils import datetimeutils


class AbstractFeedbackForm(cradmin_feedbackfeed_base.GroupCommentForm):
    """
    Feedback-related forms regarding grading inherits from this.
    """
    def get_grading_points(self):
        raise NotImplementedError()


class ExaminerBaseFeedbackFeedView(cradmin_feedbackfeed_base.FeedbackFeedBaseView):
    """
    Base view for examiner.
    """
    def get_devilryrole(self):
        """
        Get the devilryrole for the view.

        Returns:
            str: ``examiner`` as devilryrole.
        """
        return 'examiner'

    def set_automatic_attributes(self, obj):
        super(ExaminerBaseFeedbackFeedView, self).set_automatic_attributes(obj)
        obj.user_role = 'examiner'


class PassedFailedFeedbackForm(AbstractFeedbackForm):
    """
    Form for passed/failed grade plugin.
    """

    #: Set delivery as passed or failed.
    passed = forms.BooleanField(
            label=pgettext_lazy('grading', 'Passed?'),
            help_text=pgettext_lazy('grading', 'Check to provide a passing grade.'),
            initial=True,
            required=False)

    @classmethod
    def get_field_layout(cls):
        return ['passed']

    def get_grading_points(self):
        if self.cleaned_data['passed']:
            return self.group.assignment.max_points
        else:
            return 0


class PointsFeedbackForm(AbstractFeedbackForm):
    """
    Form for point-based grade plugin.
    """

    #: Set points that should be given to the delivery.
    points = forms.IntegerField(
            required=True,
            min_value=0,
            label=_('Points'))

    def __init__(self, *args, **kwargs):
        super(PointsFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['points'].max_value = self.group.assignment.max_points
        self.fields['points'].help_text = pgettext_lazy('grading', 'Number between 0 and %(max_points)s.') % {
            'max_points': self.group.assignment.max_points
        }

    @classmethod
    def get_field_layout(cls):
        return ['points']

    def get_grading_points(self):
        return self.cleaned_data['points']


class ExaminerFeedbackView(ExaminerBaseFeedbackFeedView):
    """
    The examiner feedbackview.
    This is the view where examiner corrects the delivery made by a student
    and is only able to create drafted comments, or publish grading.

    If the last FeedbackSet is published, this view redirects to :class:`.ExaminerFeedbackCreateFeedbackSetView`.
    See :func:`dispatch`.
    """
    template_name = 'devilry_group/feedbackfeed_examiner_feedback.django.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the last FeedbackSet in the group is published. If it's published, a redirect response to
        :class:`~.ExaminerFeedbackCreateFeedbackSetView is returned.

        Args:
            request: request object.

        Returns:
            HttpResponse: The HTTP response.
        """
        group = self.request.cradmin_role
        # NOTE: :func:`~devilry.apps.core.models.AssignmentGroup.last_feedbackset_is_published` performs a query.
        if group.last_feedbackset_is_published:
            return HttpResponseRedirect(self.request.cradmin_app.reverse_appurl('create-feedbackset'))
        return super(ExaminerFeedbackView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        """
        Get the correct form based on what grade plugin that is used.

        Returns:
            A :class:`devilry.devilry_group.views.cradmin_feedbackfeed_base.GroupCommentForm`

        """
        assignment = self.request.cradmin_role.assignment
        if assignment.grading_system_plugin_id == core_models.Assignment.GRADING_SYSTEM_PLUGIN_ID_PASSEDFAILED:
            return PassedFailedFeedbackForm
        elif assignment.grading_system_plugin_id == core_models.Assignment.GRADING_SYSTEM_PLUGIN_ID_POINTS:
            return PointsFeedbackForm
        else:
            raise ValueError('Unsupported grading_system_plugin_id: {}'.format(assignment.grading_system_plugin_id))

    def get_buttons(self):
        buttons = super(ExaminerFeedbackView, self).get_buttons()
        buttons.extend([
            DefaultSubmit('examiner_add_comment_to_feedback_draft',
                          _('Save draft and preview'),
                          css_class='btn btn-default'),
            PrimarySubmit('examiner_publish_feedback',
                          _('Publish feedback'),
                          css_class='btn btn-primary')
        ])
        return buttons

    def save_object(self, form, commit=True):
        comment = super(ExaminerFeedbackView, self).save_object(form=form)
        if comment.feedback_set.grading_published_datetime is not None:
            messages.warning(self.request, ugettext_lazy('Feedback is already published!'))
        else:
            if 'examiner_add_comment_to_feedback_draft' in self.request.POST:
                # If comment is part of a draft, the comment should only be visible to
                # the examiner until draft-publication.
                comment.visibility = group_models.GroupComment.VISIBILITY_PRIVATE
                comment.part_of_grading = True
                comment = super(ExaminerFeedbackView, self).save_object(form=form, commit=True)
            elif 'examiner_publish_feedback' in self.request.POST:
                result, error_msg = comment.feedback_set.publish(
                        published_by=comment.user,
                        grading_points=form.get_grading_points())
                if result is False:
                    messages.error(self.request, ugettext_lazy(error_msg))
                elif len(comment.text) > 0:
                    # Don't make comment visible to others unless it actually
                    # contains any text.
                    comment.visibility = group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE
                    comment.part_of_grading = True
                    comment.published_datetime = comment.get_published_datetime()
                    comment = super(ExaminerFeedbackView, self).save_object(form=form, commit=True)
        return comment

    def get_form_invalid_message(self, form):
        return 'Cannot publish feedback until deadline has passed!'


class ExaminerDiscussView(ExaminerBaseFeedbackFeedView):
    """
    The examiner discussview.
    This is the view examiner uses for communicating with students and admins in the feedbackfeed.
    """
    template_name = 'devilry_group/feedbackfeed_examiner_discuss.django.html'

    def get_buttons(self):
        buttons = super(ExaminerDiscussView, self).get_buttons()
        buttons.extend([
            PrimarySubmit('examiner_add_comment_for_examiners',
                          _('Add comment for examiners'),
                          css_class='btn btn-default'),
            DefaultSubmit('examiner_add_public_comment',
                          _('Add public comment'),
                          css_class='btn btn-primary'),
        ])
        return buttons

    def save_object(self, form, commit=True):
        comment = super(ExaminerDiscussView, self).save_object(form)
        self._convert_temporary_files_to_comment_files(form, comment)
        if form.data.get('examiner_add_comment_for_examiners'):
            comment.visibility = group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS
            comment.published_datetime = timezone.now()
        elif form.data.get('examiner_add_public_comment'):
            comment.visibility = group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE
            comment.published_datetime = timezone.now()

        comment = super(ExaminerDiscussView, self).save_object(form, commit=True)
        return comment

    def get_success_url(self):
        return self.request.cradmin_app.reverse_appurl(viewname='discuss')


class EditGroupCommentForm(forms.ModelForm):
    """
    Form for editing existing Feedback drafts.
    """
    class Meta:
        fields = ['text']
        model = group_models.GroupComment

    @classmethod
    def get_field_layout(cls):
        return ['text']


class CreateFeedbackSetForm(cradmin_feedbackfeed_base.GroupCommentForm):
    """
    Form for creating a new FeedbackSet (deadline).
    """
    #: Deadline to be added to the new FeedbackSet.
    deadline_datetime = forms.DateTimeField(widget=DateTimePickerWidget)

    @classmethod
    def get_field_layout(cls):
        return ['deadline_datetime']


class ExaminerFeedbackCreateFeedbackSetView(ExaminerBaseFeedbackFeedView):
    """
    View to create a new FeedbackSet if the current last feedbackset is published.

    When a new unpublished FeedbackSet is created, this view redirects to :class:`.ExaminerFeedbackView`.
    See :func:`dispatch`.
    """
    template_name = 'devilry_group/feedbackfeed_examiner_feedback.django.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the last FeedbackSet in the group is published. If it's published, a redirect response to
        :class:`~.ExaminerFeedbackView` is returned.

        Args:
            request (HttpRequest): request object.

        Returns:
            HttpResponse: The HTTP response.
        """
        group = self.request.cradmin_role
        # NOTE: :func:`~devilry.apps.core.models.AssignmentGroup.last_feedbackset_is_published` performs a query.
        if not group.last_feedbackset_is_published:
            return HttpResponseRedirect(self.request.cradmin_app.reverse_appindexurl())
        return super(ExaminerFeedbackCreateFeedbackSetView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return CreateFeedbackSetForm

    def get_buttons(self):
        buttons = super(ExaminerFeedbackCreateFeedbackSetView, self).get_buttons()
        buttons.extend([
            DefaultSubmit('examiner_create_new_feedbackset',
                          _('Give new attempt'),
                          css_class='btn btn-primary'),
        ])
        return buttons

    @staticmethod
    def __update_current_feedbackset(comment):
        """
        Get the current :obj:`~devilry.devilry_group.models.FeedbackSet` from ``comment``, update it's fields and
        save it the changes.

        Args:
            comment (GroupComment): Get :obj:`~devilry.devilry_group.models.FeedbackSet` from.
        """
        current_feedbackset = group_models.FeedbackSet.objects.get(id=comment.feedback_set_id)
        current_feedbackset.grading_published_by = comment.user
        current_feedbackset.full_clean()
        current_feedbackset.save()

    def __create_new_feedbackset(self, comment, new_deadline):
        """
        Creates a new :class:`devilry.devilry_group.models.FeedbackSet` as long as the ``new_deadline`` is
        in the future.

        :Note: Extra constraints to the new deadline and creation of a FeedbackSet may be added.

        Args:
            comment (GroupComment): Comment to be posted with the new FeedbackSet
            new_deadline (DateTime): The deadline.

        Returns:
            FeedbackSet: returns the newly created :class:`devilry.devilry_group.models.FeedbackSet` instance.

        """
        # Make sure the deadline is in the future.
        if new_deadline <= datetimeutils.get_current_datetime():
            messages.error(self.request, ugettext_lazy('Deadline must be ahead of current date and time'))
            return None

        # Update current last feedbackset in group before
        # creating the new feedbackset.
        self.__update_current_feedbackset(comment)

        # Create a new :class:`~devilry.devilry_group.models.FeedbackSet` and save it.
        feedbackset = group_models.FeedbackSet(
            group=self.request.cradmin_role,
            feedbackset_type=group_models.FeedbackSet.FEEDBACKSET_TYPE_NEW_ATTEMPT,
            created_by=comment.user,
            deadline_datetime=new_deadline
        )
        feedbackset.full_clean()
        feedbackset.save()
        return feedbackset

    def save_object(self, form, commit=True):
        comment = super(ExaminerFeedbackCreateFeedbackSetView, self).save_object(form=form)

        if 'deadline_datetime' in self.request.POST:
            new_deadline = datetime.strptime(self.request.POST['deadline_datetime'], '%Y-%m-%d %H:%M')
            # Create a new :obj:`~devilry.devilry_group.models.FeedbackSet`.
            new_feedbackset = self.__create_new_feedbackset(comment=comment, new_deadline=new_deadline)
            if new_feedbackset is None:
                return comment

            if len(comment.text) > 0:
                # Also save comment and set the comments feedback_set to the newly
                # created new_feedbackset.
                comment.visibility = group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE
                comment.feedback_set = new_feedbackset
                comment.published_datetime = new_feedbackset.created_datetime + timezone.timedelta(seconds=1)
                comment = super(ExaminerFeedbackCreateFeedbackSetView, self).save_object(form=form, commit=True)
        return comment


class GroupCommentEditDeleteMixin(object):
    """
    Basic mixin/super-class for GroupCommentDeleteView and GroupCommentEditView.
    """
    model = group_models.GroupComment

    class Meta:
        abstract = True

    def get_queryset_for_role(self, role):
        """
        Filter out :obj:`~devilry.devilry_group.models.GroupComment`s based on the role of role of the
        crinstance and the primarykey of the comment since in this case only a single comment should be fetched.

        Args:
            role (GroupComment): The roleclass for the crinstance.

        Returns:
            QuerySet: Set containing one :obj:`~devilry.devilry_group.models.GroupComment`.
        """
        return group_models.GroupComment.objects.filter(
                feedback_set__group=role,
                id=self.kwargs.get('pk')).exclude_comment_is_not_draft_from_user(self.request.user)


class GroupCommentDeleteView(GroupCommentEditDeleteMixin, delete.DeleteView):
    """
    View for deleting an existing groupcomment with visibility set to private.
    When a groupcomment has visibility set to private, this means it's a feedbackdraft.
    """
    template_name = 'devilry_group/feedbackfeed_examiner_delete_groupcomment.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the GroupComment id passed is for a drafted comment.
        If the comment is not a draft, PermissionDenied is raised.

        Args:
            request (HttpRequest): request object.

        Returns:
            HttpResponseRedirect: Reponse redirect object.

        Raises:
            PermissionDenied: If comment is not a draft, this exception is raised.
        """
        if len(self.get_queryset_for_role(request.cradmin_role)) == 0:
            raise PermissionDenied
        return super(GroupCommentDeleteView, self).dispatch(request, *args, **kwargs)

    def get_object_preview(self):
        return 'Groupcomment'

    def get_success_url(self):
        return self.request.cradmin_app.reverse_appindexurl()


class GroupCommentEditView(GroupCommentEditDeleteMixin, update.UpdateView):
    """
    View to edit an existing feedback draft.

    Makes it possible for an Examiner to edit the ``text``-attribute value of a
    :class:`~devilry.devilry_group.models.GroupComment` that's saved as a draft.
    """
    template_name = 'devilry_group/feedbackfeed_examiner_edit_groupcomment.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the GroupComment id passed is for a drafted comment.
        If the comment is not a draft, PermissionDenied is raised.

        Args:
            request (HttpRequest): request object.

        Returns:
            HttpResponseRedirect: Reponse redirect object.

        Raises:
            PermissionDenied: If comment is not a draft, this exception is raised.
        """
        if len(self.get_queryset_for_role(request.cradmin_role)) == 0:
            raise PermissionDenied
        return super(GroupCommentEditView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        """
        Get the formclass to use.

        Returns:
            EditGroupCommentForm: The form class.
        """
        return EditGroupCommentForm

    def get_form(self, form_class=None):
        """
        Set ``AceMarkdownWidget`` on the text form field and do not show the field label.
        Args:
            form_class: Defaults to None

        Returns:
            EditGroupCommentForm: Form with field-representations set.
        """
        form = super(GroupCommentEditView, self).get_form(form_class=form_class)
        form.fields['text'].widget = AceMarkdownWidget()
        form.fields['text'].label = False
        return form

    def get_field_layout(self):
        """
        Override get field layout as we're using ``AceMarkdownWidget`` to define
        the form field in our form class :class:`~.EditGroupCommentForm`.

        Returns:
            list: List extended with the field layout of :class:`~.EditGroupCommentForm`.
        """
        field_layout = []
        field_layout.extend(self.get_form_class().get_field_layout())
        return field_layout

    def save_object(self, form, commit=True):
        """
        Save the edited :obj:`~devilry.devilry_group.models.GroupComment`.

        Args:
            form: The :class:`~.EditGroupCommentForm` passed.
            commit: Should it be saved? (Defaults to True)

        Returns:
            GroupComment: The saved comment.
        """
        comment = super(GroupCommentEditView, self).save_object(form=form, commit=commit)
        self.add_success_messages('GroupComment updated!')
        return comment

    def get_success_url(self):
        """
        The success url is for this view if the user wants to continue editing, else it redirects to
        the indexview, :class:`~.ExaminerFeedbackView`.

        Returns:
            url: Redirected to view for that url.
        """
        if self.get_submit_save_and_continue_edititing_button_name() in self.request.POST:
            return self.request.cradmin_app.reverse_appurl(
                'groupcomment-edit',
                args=self.args,
                kwargs=self.kwargs)
        else:
            return self.request.cradmin_app.reverse_appindexurl()


class App(crapp.App):
    appurls = [
        crapp.Url(
                r'^$',
                ExaminerFeedbackView.as_view(),
                name=crapp.INDEXVIEW_NAME),
        crapp.Url(
                r'^discuss$',
                ExaminerDiscussView.as_view(),
                name='discuss'),
        crapp.Url(
                r'^create-feedbackset$',
                ExaminerFeedbackCreateFeedbackSetView.as_view(),
                name='create-feedbackset'),
        crapp.Url(
                r'^groupcomment-delete/(?P<pk>\d+)$',
                GroupCommentDeleteView.as_view(),
                name="groupcomment-delete"),
        crapp.Url(
                r'^groupcomment-edit/(?P<pk>\d+)$',
                GroupCommentEditView.as_view(),
                name='groupcomment-edit'),
    ]
