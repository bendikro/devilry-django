from django.utils import timezone
from django.test import TestCase
from model_mommy import mommy

from devilry.devilry_group import models
from devilry.devilry_group.models import GroupComment
from devilry.devilry_group.tests import test_feedbackfeed_common
from devilry.devilry_group.views import feedbackfeed_examiner


class TestFeedbackfeedExaminer(TestCase, test_feedbackfeed_common.TestFeedbackFeedMixin):
    viewclass = feedbackfeed_examiner.ExaminerFeedbackFeedView

    def test_get(self):
        examiner = mommy.make('core.Examiner')
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=examiner.assignmentgroup,
                                                          requestuser=examiner.user)
        self.assertEquals(mockresponse.selector.one('title').alltext_normalized,
                          examiner.assignmentgroup.assignment.get_path())

    def test_get_feedbackfeed_examiner_wysiwyg_get_comment_choise_add_comment_for_examiners_and_admins_button(self):
        examiner = mommy.make('core.Examiner')
        feedbackset = mommy.make('devilry_group.FeedbackSet', group=examiner.assignmentgroup)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=feedbackset.group,
                                                          requestuser=examiner.user)
        self.assertTrue(mockresponse.selector.exists('#submit-id-examiner_add_comment_for_examiners'))

    def test_get_feedbackfeed_examiner_wysiwyg_get_comment_choise_add_comment_public_button(self):
        examiner = mommy.make('core.Examiner')
        feedbackset = mommy.make('devilry_group.FeedbackSet', group=examiner.assignmentgroup)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=feedbackset.group,
                                                          requestuser=examiner.user)
        self.assertTrue(mockresponse.selector.exists('#submit-id-examiner_add_public_comment'))

    def test_get_feedbackfeed_examiner_wysiwyg_get_comment_choise_add_comment_to_feedbackdraft_button(self):
        examiner = mommy.make('core.Examiner')
        feedbackset = mommy.make('devilry_group.FeedbackSet', group=examiner.assignmentgroup)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=feedbackset.group,
                                                          requestuser=examiner.user)
        self.assertTrue(mockresponse.selector.exists('#submit-id-examiner_add_comment_to_feedback_draft'))

    def test_get_admin_can_see_student_comment(self):
        group = mommy.make('core.AssignmentGroup')
        student = mommy.make('core.Candidate', assignment_group=group, student__fullname='Jane Doe')
        examiner = mommy.make('core.Examiner', assignmentgroup=group)
        mommy.make('devilry_group.GroupComment',
                   user=student.student,
                   user_role='student',
                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                   published_datetime=timezone.now() - timezone.timedelta(days=1),
                   feedback_set__group=group)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=examiner.assignmentgroup,
                                                          requestuser=examiner.user)
        name = mockresponse.selector.one('.devilry-user-verbose-inline-fullname').alltext_normalized
        self.assertEquals(student.student.fullname, name)

    def test_post_feedbackset_comment_with_text(self):
        feedbackset = mommy.make('devilry_group.FeedbackSet')
        examiner = mommy.make('core.Examiner', assignmentgroup=feedbackset.group)
        self.mock_http302_postrequest(
            cradmin_role=examiner.assignmentgroup,
            viewkwargs={'pk': feedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(1, len(models.GroupComment.objects.all()))

    def test_post_feedbackset_comment_without_text(self):
        feedbackset = mommy.make('devilry_group.FeedbackSet')
        examiner = mommy.make('core.Examiner', assignmentgroup=feedbackset.group)
        self.mock_http302_postrequest(
            cradmin_role=examiner.assignmentgroup,
            viewkwargs={'pk': feedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                }
            })
        self.assertEquals(0, len(models.GroupComment.objects.all()))
