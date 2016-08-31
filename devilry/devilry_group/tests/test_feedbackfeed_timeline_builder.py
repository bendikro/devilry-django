import mock
from django.test import TestCase
from django.utils import timezone
from django.conf import settings

from model_mommy import mommy

from devilry.devilry_dbcache.customsql import AssignmentGroupDbCacheCustomSql
from devilry.devilry_group import devilry_group_mommy_factories as group_mommy
from devilry.devilry_group.timeline_builder.feedbackfeed_timeline_builder import FeedbackFeedTimelineBuilder
from devilry.devilry_group import models as group_models


class TestFeedbackFeedTimelineBuilder(TestCase, object):

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def test_get_last_deadline_one_feedbackset(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)
        mommy.make('devilry_group.FeedbackSet', group=group)
        timelinebuilder = FeedbackFeedTimelineBuilder(group=group, requestuser=testuser, devilryrole='unused')
        timelinebuilder.build()
        self.assertEquals(2, len(timelinebuilder.feedbacksets))
        self.assertEquals(assignment.first_deadline, timelinebuilder.get_last_deadline())

    def test_get_last_deadline_two_feedbackset(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)
        feedbackset_last = mommy.make('devilry_group.FeedbackSet',
                                      group=group,
                                      deadline_datetime=timezone.now(),
                                      feedbackset_type=group_models.FeedbackSet.FEEDBACKSET_TYPE_NEW_ATTEMPT)
        timelinebuilder = FeedbackFeedTimelineBuilder(group=group, requestuser=testuser, devilryrole='unused')
        timelinebuilder.build()
        self.assertEquals(2, len(timelinebuilder.feedbacksets))
        self.assertEquals(feedbackset_last.deadline_datetime, timelinebuilder.get_last_deadline())

    def test_get_num_elements_in_timeline(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)
        now = timezone.now()
        group_mommy.feedbackset_first_attempt_published(
                group=group,
                created_datetime=now - timezone.timedelta(days=20),
                grading_published_datetime=now-timezone.timedelta(days=19))
        group_mommy.feedbackset_new_attempt_published(
                group=group,
                created_datetime=now - timezone.timedelta(days=18),
                deadline_datetime=now-timezone.timedelta(days=17),
                grading_published_datetime=now-timezone.timedelta(days=16))
        group_mommy.feedbackset_new_attempt_published(
                group=group,
                created_datetime=now - timezone.timedelta(days=15),
                deadline_datetime=now-timezone.timedelta(days=14),
                grading_published_datetime=now-timezone.timedelta(days=13))
        group_mommy.feedbackset_new_attempt_published(
                group=group,
                created_datetime=now - timezone.timedelta(days=12),
                deadline_datetime=now-timezone.timedelta(days=11),
                grading_published_datetime=now-timezone.timedelta(days=10))
        timelinebuilder = FeedbackFeedTimelineBuilder(group=group, requestuser=testuser, devilryrole='unused')
        timelinebuilder.build()

        self.assertEquals(11, len(timelinebuilder.timeline))

    def test_get_last_feedbackset(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)
        now = timezone.now()
        group_mommy.feedbackset_first_attempt_published(
                group=group,
                grading_published_datetime=now-timezone.timedelta(days=10))
        feedbackset_last = group_mommy.feedbackset_new_attempt_published(
                group=group,
                deadline_datetime=now-timezone.timedelta(days=9),
                grading_published_datetime=now-timezone.timedelta(days=8))
        timelinebuilder = FeedbackFeedTimelineBuilder(group=group, requestuser=testuser, devilryrole='unused')
        timelinebuilder.build()
        self.assertEquals(feedbackset_last, timelinebuilder.get_last_feedbackset())

    def test_get_last_deadline(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)
        now = timezone.now()
        group_mommy.feedbackset_first_attempt_published(
                group=group,
                grading_published_datetime=now-timezone.timedelta(days=10))
        feedbackset_last = group_mommy.feedbackset_new_attempt_published(
                group=group,
                deadline_datetime=now-timezone.timedelta(days=9),
                grading_published_datetime=now-timezone.timedelta(days=8))
        timelinebuilder = FeedbackFeedTimelineBuilder(group=group, requestuser=testuser, devilryrole='unused')
        timelinebuilder.build()
        self.assertEquals(feedbackset_last.deadline_datetime, timelinebuilder.get_last_deadline())

    def test_get_visibility_for_roles_not_published(self):
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)

        examiner = mommy.make('core.Examiner',
                              assignmentgroup=group,
                              relatedexaminer__user=mommy.make(settings.AUTH_USER_MODEL))
        examiner2 = mommy.make('core.Examiner',
                               assignmentgroup=group,
                               relatedexaminer__user=mommy.make(settings.AUTH_USER_MODEL))
        candidate = mommy.make('core.Candidate',
                               assignment_group=group,
                               relatedstudent__user=mommy.make(settings.AUTH_USER_MODEL))

        feedbackset = group_mommy.feedbackset_first_attempt_unpublished(group=group)
        mommy.make('devilry_group.GroupComment',
                   user=examiner.relatedexaminer.user,
                   user_role=group_models.GroupComment.USER_ROLE_EXAMINER,
                   feedback_set=feedbackset)
        mommy.make('devilry_group.GroupComment',
                   user=examiner.relatedexaminer.user,
                   user_role=group_models.GroupComment.USER_ROLE_EXAMINER,
                   part_of_grading=True,
                   feedback_set=feedbackset)
        mommy.make('devilry_group.GroupComment',
                   user=candidate.relatedstudent.user,
                   user_role=group_models.GroupComment.USER_ROLE_STUDENT,
                   feedback_set=feedbackset)
        mommy.make('devilry_group.GroupComment',
                   user=candidate.relatedstudent.user,
                   user_role=group_models.GroupComment.USER_ROLE_STUDENT,
                   feedback_set=feedbackset)
        mommy.make('devilry_group.GroupComment',
                   user=examiner.relatedexaminer.user,
                   user_role=group_models.GroupComment.USER_ROLE_EXAMINER,
                   visibility=group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                   feedback_set=feedbackset)
        mommy.make('devilry_group.GroupComment',
                   user=examiner.relatedexaminer.user,
                   user_role=group_models.GroupComment.USER_ROLE_EXAMINER,
                   visibility=group_models.GroupComment.VISIBILITY_PRIVATE,
                   feedback_set=feedbackset)

        # examiner can see all comments
        timelinebuilder_examiner = FeedbackFeedTimelineBuilder(
                group=group,
                requestuser=examiner.relatedexaminer.user,
                devilryrole='examiner')
        timelinebuilder_examiner.build()
        self.assertEquals(6, len(timelinebuilder_examiner.feedbacksets[1].groupcomment_set.all()))
        self.assertEquals(7, len(timelinebuilder_examiner.timeline))

        # examiner2 can see all comments, except private comments
        timelinebuilder_examiner2 = FeedbackFeedTimelineBuilder(
                group=group,
                requestuser=examiner2.relatedexaminer.user,
                devilryrole='examiner')
        timelinebuilder_examiner2.build()
        self.assertEquals(5, len(timelinebuilder_examiner2.feedbacksets[1].groupcomment_set.all()))
        self.assertEquals(6, len(timelinebuilder_examiner2.timeline))

        # student can only see what is visible to everyone(VISIBILITY_VISIBLE_TO_EVERYONE)
        timelinebuilder_student = FeedbackFeedTimelineBuilder(
            group=group,
            requestuser=candidate.relatedstudent.user,
            devilryrole='student'
        )
        timelinebuilder_student.build()
        self.assertEquals(3, len(timelinebuilder_student.feedbacksets[1].groupcomment_set.all()))
        self.assertEquals(4, len(timelinebuilder_student.timeline))

    def test_get_one_group(self):
        assignment1 = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        assignment2 = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group1 = mommy.make('core.AssignmentGroup', parentnode=assignment1)
        group2 = mommy.make('core.AssignmentGroup', parentnode=assignment2)
        relatedstudent = mommy.make('core.RelatedStudent')
        mommy.make('core.Candidate',
                   assignment_group=group1,
                   relatedstudent=relatedstudent)
        mommy.make('core.Candidate',
                   assignment_group=group2,
                   relatedstudent=relatedstudent)
        feedbackset = group_mommy.feedbackset_first_attempt_unpublished(group=group1)
        group_mommy.feedbackset_first_attempt_unpublished(group=group2)

        timelinebuilder = FeedbackFeedTimelineBuilder(
            group=group1,
            requestuser=relatedstudent.user,
            devilryrole='student'
        )
        self.assertEquals(2, len(timelinebuilder.feedbacksets))
        self.assertEquals(feedbackset, timelinebuilder.feedbacksets[1])

    def test_complete_example(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        candidate = mommy.make('core.Candidate',
                               assignment_group=testgroup,
                               relatedstudent__user__fullname='Test User1',
                               relatedstudent__user__shortname='testuser1@example.com')
        examiner = mommy.make('core.Examiner',
                              assignmentgroup=testgroup,
                              relatedexaminer_user__fullname='Test User2',
                              relatedexaminer__user__shortname='testuser2@example.com')

        # First feedbackset published with comments and grading
        testfeedbackset1 = group_mommy.feedbackset_first_attempt_published(
                grading_published_datetime=testassignment.first_deadline + timezone.timedelta(days=1),
                grading_points=10,
                created_by=examiner.relatedexaminer.user,
                created_datetime=testassignment.publishing_time,
                group=testgroup,
                grading_published_by=examiner.relatedexaminer.user)
        mommy.make('devilry_group.GroupComment',
                   created_datetime=testfeedbackset1.current_deadline() - timezone.timedelta(hours=1),
                   published_datetime=testfeedbackset1.current_deadline() - timezone.timedelta(hours=1),
                   user=candidate.relatedstudent.user,
                   user_role='student',
                   feedback_set=testfeedbackset1)
        mommy.make('devilry_group.GroupComment',
                   created_datetime=testfeedbackset1.current_deadline() + timezone.timedelta(hours=1),
                   published_datetime=testfeedbackset1.current_deadline() + timezone.timedelta(hours=1),
                   user=examiner.relatedexaminer.user,
                   user_role='examiner',
                   part_of_grading=True,
                   feedback_set=testfeedbackset1)

        # Second feedbackset with comments and grading
        testfeedbackset2 = group_mommy.feedbackset_new_attempt_published(
                grading_published_datetime=testfeedbackset1.grading_published_datetime + timezone.timedelta(days=4),
                grading_points=10,
                created_datetime=testfeedbackset1.grading_published_datetime + timezone.timedelta(hours=10),
                deadline_datetime=testfeedbackset1.grading_published_datetime + timezone.timedelta(days=3),
                created_by=examiner.relatedexaminer.user,
                group=testgroup,
                grading_published_by=examiner.relatedexaminer.user)
        mommy.make('devilry_group.GroupComment',
                   created_datetime=testfeedbackset2.current_deadline() - timezone.timedelta(hours=1),
                   published_datetime=testfeedbackset2.current_deadline() - timezone.timedelta(hours=1),
                   user=candidate.relatedstudent.user,
                   user_role='student',
                   feedback_set=testfeedbackset2)
        mommy.make('devilry_group.GroupComment',
                   created_datetime=testfeedbackset2.current_deadline() + timezone.timedelta(hours=1),
                   published_datetime=testfeedbackset2.current_deadline() + timezone.timedelta(hours=1),
                   user=examiner.relatedexaminer.user,
                   user_role='examiner',
                   part_of_grading=True,
                   feedback_set=testfeedbackset2)

        built_timeline = FeedbackFeedTimelineBuilder(
            group=testgroup,
            requestuser=testuser,
            devilryrole='student'
        )

        built_timeline.build()
        builder_list = built_timeline.get_as_list()

        self.assertEquals(builder_list[0]['type'], 'comment')
        self.assertEquals(builder_list[1]['type'], 'deadline_expired')
        self.assertEquals(builder_list[2]['type'], 'deadline_expired')
        self.assertEquals(builder_list[3]['type'], 'comment')
        self.assertEquals(builder_list[4]['type'], 'grade')
        self.assertEquals(builder_list[5]['type'], 'deadline_created')
        self.assertEquals(builder_list[6]['type'], 'comment')
        self.assertEquals(builder_list[7]['type'], 'deadline_expired')
        self.assertEquals(builder_list[8]['type'], 'comment')
        self.assertEquals(builder_list[9]['type'], 'grade')
