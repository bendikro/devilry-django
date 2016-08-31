from __future__ import unicode_literals

from django.db import models
from django.db.models.functions import Lower, Concat
from django_cradmin import crapp
from django_cradmin.crinstance import reverse_cradmin_url
from django_cradmin.viewhelpers import listbuilderview

from devilry.apps.core import models as coremodels
from devilry.apps.core.models import Candidate, Examiner, RelatedExaminer
from devilry.devilry_cradmin import devilry_listbuilder
from devilry.devilry_cradmin import devilry_listfilter


class GroupItemFrame(devilry_listbuilder.common.GoForwardLinkItemFrame):
    valuealias = 'group'

    def get_url(self):
        return reverse_cradmin_url(
            instanceid='devilry_group_examiner',
            appname='feedbackfeed',
            roleid=self.group.id,
            viewname=crapp.INDEXVIEW_NAME,
        )


class GroupListView(listbuilderview.FilterListMixin,
                    listbuilderview.View):
    model = coremodels.AssignmentGroup
    value_renderer_class = devilry_listbuilder.assignmentgroup.ExaminerItemValue
    frame_renderer_class = GroupItemFrame

    def dispatch(self, request, *args, **kwargs):
        self.assignment = self.request.cradmin_role
        return super(GroupListView, self).dispatch(request, *args, **kwargs)

    def get_filterlist_template_name(self):
        return 'devilry_examiner/assignment/grouplist.django.html'

    def get_pagetitle(self):
        return self.assignment.long_name

    def get_filterlist_url(self, filters_string):
        return self.request.cradmin_app.reverse_appurl(
            'filter',
            kwargs={'filters_string': filters_string})

    def get_value_and_frame_renderer_kwargs(self):
        return {
            'assignment': self.assignment
        }

    def __add_filterlist_items_anonymous_uses_custom_candidate_ids(self, filterlist):
        filterlist.append(devilry_listfilter.assignmentgroup.SearchAnonymousUsesCustomCandidateIds())
        filterlist.append(devilry_listfilter.assignmentgroup.OrderByAnonymousUsesCustomCandidateIds())

    def __add_filterlist_items_anonymous(self, filterlist):
        filterlist.append(devilry_listfilter.assignmentgroup.SearchAnonymous())
        filterlist.append(devilry_listfilter.assignmentgroup.OrderByAnonymous())

    def __add_filterlist_items_not_anonymous(self, filterlist):
        filterlist.append(devilry_listfilter.assignmentgroup.SearchNotAnonymous())
        filterlist.append(devilry_listfilter.assignmentgroup.OrderByNotAnonymous())

    def add_filterlist_items(self, filterlist):
        if self.assignment.is_anonymous:
            if self.assignment.uses_custom_candidate_ids:
                self.__add_filterlist_items_anonymous_uses_custom_candidate_ids(filterlist=filterlist)
            else:
                self.__add_filterlist_items_anonymous(filterlist=filterlist)
        else:
            self.__add_filterlist_items_not_anonymous(filterlist=filterlist)
        filterlist.append(devilry_listfilter.assignmentgroup.StatusRadioFilter(view=self))
        filterlist.append(devilry_listfilter.assignmentgroup.IsPassingGradeFilter())
        filterlist.append(devilry_listfilter.assignmentgroup.PointsFilter())
        if self.__has_multiple_examiners():
            filterlist.append(devilry_listfilter.assignmentgroup.ExaminerFilter(view=self))
        filterlist.append(devilry_listfilter.assignmentgroup.ActivityFilter())

    def get_unfiltered_queryset_for_role(self, role):
        assignment = role
        candidatequeryset = Candidate.objects\
            .select_related('relatedstudent__user')\
            .only(
                'candidate_id',
                'assignment_group',
                'relatedstudent__candidate_id',
                'relatedstudent__automatic_anonymous_id',
                'relatedstudent__user__shortname',
                'relatedstudent__user__fullname',
            )\
            .order_by(
                Lower(Concat('relatedstudent__user__fullname',
                             'relatedstudent__user__shortname')))
        examinerqueryset = Examiner.objects\
            .select_related('relatedexaminer__user')\
            .only(
                'relatedexaminer',
                'assignmentgroup',
                'relatedexaminer__automatic_anonymous_id',
                'relatedexaminer__user__shortname',
                'relatedexaminer__user__fullname',
            )\
            .order_by(
                Lower(Concat('relatedexaminer__user__fullname',
                             'relatedexaminer__user__shortname')))
        queryset = coremodels.AssignmentGroup.objects\
            .filter_examiner_has_access(user=self.request.user)\
            .filter(parentnode=assignment)\
            .only('name')\
            .prefetch_related(
                models.Prefetch('candidates',
                                queryset=candidatequeryset))\
            .prefetch_related(
                models.Prefetch('examiners',
                                queryset=examinerqueryset))\
            .annotate_with_grading_points()\
            .annotate_with_is_waiting_for_feedback()\
            .annotate_with_is_waiting_for_deliveries()\
            .annotate_with_is_corrected()\
            .annotate_with_number_of_commentfiles_from_students()\
            .annotate_with_number_of_groupcomments_from_students()\
            .annotate_with_number_of_groupcomments_from_examiners()\
            .annotate_with_number_of_groupcomments_from_admins()\
            .annotate_with_number_of_imageannotationcomments_from_students()\
            .annotate_with_number_of_imageannotationcomments_from_examiners()\
            .annotate_with_number_of_imageannotationcomments_from_admins()\
            .annotate_with_has_unpublished_feedbackdraft()\
            .annotate_with_number_of_private_groupcomments_from_user(user=self.request.user)\
            .annotate_with_number_of_private_imageannotationcomments_from_user(user=self.request.user)\
            .distinct()
        return queryset

    def __get_status_filter_value(self):
        status_value = self.get_filterlist().filtershandler.get_cleaned_value_for('status')
        if not status_value:
            status_value = 'all'
        return status_value

    def __get_unfiltered_queryset_for_role(self):
        #print "__get_unfiltered_queryset_for_role"
        import traceback
        #traceback.print_stack(limit=2)
        return self.get_unfiltered_queryset_for_role(role=self.request.cradmin_role)

    def __get_total_groupcount(self):
        return self.__get_unfiltered_queryset_for_role().count()

    # def __get_filtered_groupcount(self):
    #     return self.get_queryset().count()

    def __get_excluding_filters_other_than_status_is_applied(self, total_groupcount):
        return self.get_filterlist().filter(
            queryobject=self.__get_unfiltered_queryset_for_role(),
            exclude={'status'}
        ).count() < total_groupcount

    def get_filtered_all_students_count(self):
        return self.get_filterlist()\
            .filter(queryobject=self.__get_unfiltered_queryset_for_role(),
                    exclude={'status'})\
            .count()

    def get_filtered_waiting_for_feedback_count(self):
        return self.get_filterlist()\
            .filter(queryobject=self.__get_unfiltered_queryset_for_role(),
                    exclude={'status'})\
            .filter(is_waiting_for_feedback=True)\
            .count()

    def get_filtered_waiting_for_deliveries_count(self):
        print "get_filtered_waiting_for_deliveries_count:",  self.get_filterlist()\
            .filter(queryobject=self.__get_unfiltered_queryset_for_role(),
                    exclude={'status'})\
            .filter(is_waiting_for_deliveries=True)\
            .count()

        return self.get_filterlist()\
            .filter(queryobject=self.__get_unfiltered_queryset_for_role(),
                    exclude={'status'})\
            .filter(is_waiting_for_deliveries=True)\
            .count()

    def get_filtered_corrected_count(self):
        return self.get_filterlist()\
            .filter(queryobject=self.__get_unfiltered_queryset_for_role(),
                    exclude={'status'})\
            .filter(is_corrected=True)\
            .count()

    def __get_distinct_relatedexaminer_ids(self):
        #print "__get_distinct_relatedexaminer_ids"
        if not hasattr(self, '_distinct_relatedexaminer_ids'):
            self._distinct_relatedexaminer_ids = Examiner.objects\
                .filter(assignmentgroup__in=self.__get_unfiltered_queryset_for_role())\
                .values_list('relatedexaminer_id', flat=True)\
                .distinct()
            self._distinct_relatedexaminer_ids = list(self._distinct_relatedexaminer_ids)
        return self._distinct_relatedexaminer_ids

    def __has_multiple_examiners(self):
        return len(self.__get_distinct_relatedexaminer_ids()) > 1

    def get_distinct_relatedexaminers(self):
        #print "get_distinct_relatedexaminers"
        return RelatedExaminer.objects\
            .filter(id__in=self.__get_distinct_relatedexaminer_ids())\
            .select_related('user')\
            .order_by(Lower(Concat('user__fullname', 'user__shortname')))

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['status_filter_value_normalized'] = self.__get_status_filter_value()
        total_groupcount = self.__get_total_groupcount()
        context['excluding_filters_other_than_status_is_applied'] = \
            self.__get_excluding_filters_other_than_status_is_applied(
                total_groupcount=total_groupcount)
        return context


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$',
                  GroupListView.as_view(),
                  name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^filter/(?P<filters_string>.+)?$',
                  GroupListView.as_view(),
                  name='filter'),
    ]
