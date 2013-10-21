from datetime import datetime
from djangorestframework.views import ModelView
from djangorestframework.mixins import InstanceMixin
from djangorestframework.mixins import ReadModelMixin
from djangorestframework.resources import ModelResource
from djangorestframework.permissions import IsAuthenticated

from devilry.apps.core.models import AssignmentGroup
from .helpers import format_datetime
from .helpers import format_timedelta
from .helpers import GroupResourceHelpersMixin
from .helpers import IsPublishedAndCandidate

from devilry.apps.core.serialize.candidate import serialize_candidate
from devilry.apps.core.serialize.delivery import serialize_delivery
from devilry.apps.core.serialize.feedback import serialize_feedback




class GroupResource(ModelResource, GroupResourceHelpersMixin):
    fields = ('id', 'name', 'is_open', 'candidates', 'deadlines', 'active_feedback',
              'deadline_handling', 'breadcrumbs', 'examiners', 'delivery_types',
              'status', 'is_relatedstudent_on_period')
    model = AssignmentGroup


    def candidates(self, instance):
        return map(serialize_candidate, instance.candidates.all())

    def format_feedback(self, staticfeedback, anonymous):
        return serialize_feedback(staticfeedback, without_points=True, anonymous=anonymous)

    def format_delivery(self, delivery, anonymous):
        return serialize_delivery(delivery, without_points=True, anonymous=anonymous)

    def format_deliveries(self, deadline, anonymous):
        return map(lambda d: self.format_delivery(d, anonymous), deadline.deliveries.filter(successful=True))

    def format_deadline(self, deadline, anonymous):
        now = datetime.now()
        return {'id': deadline.id,
                'deadline': format_datetime(deadline.deadline),
                'in_the_future': deadline.deadline > now,
                'offset_from_now': format_timedelta(now - deadline.deadline),
                'text': deadline.text,
                'deliveries': self.format_deliveries(deadline, anonymous)}

    def deadlines(self, instance):
        return map(lambda d: self.format_deadline(d, instance.parentnode.anonymous), instance.deadlines.all())

    def active_feedback(self, instance):
        """
        The active feedback is the feedback that was saved last.
        """
        if instance.feedback:
            return {'feedback': self.format_feedback(instance.feedback, anonymous=instance.parentnode.anonymous),
                    'deadline_id': instance.feedback.delivery.deadline_id,
                    'delivery_id': instance.feedback.delivery_id}
        else:
            return None

    def deadline_handling(self, instance):
        return instance.parentnode.deadline_handling

    def breadcrumbs(self, instance):
        return {'assignment': self.format_basenode(instance.parentnode),
                'period': self.format_basenode(instance.parentnode.parentnode),
                'subject': self.format_basenode(instance.parentnode.parentnode.parentnode)}


    def examiners(self, instance):
        if instance.parentnode.anonymous:
            return None
        else:
            return map(self.format_examiner, instance.examiners.all())

    def delivery_types(self, instance):
        return instance.parentnode.delivery_types

    def status(self, instance):
        return instance.get_status()

    def is_relatedstudent_on_period(self, instance):
        period = instance.parentnode.parentnode
        user = self.view.request.user
        return period.relatedstudent_set.filter(user=user).exists()

class AggregatedGroupInfo(InstanceMixin, ReadModelMixin, ModelView):
    """
    Provides an API that aggregates a lot of information about a group.

    # GET
    An object with the following attributes:

    - ``id`` (int): Internal Devilry ID of the group. Is never ``null``.
    - ``name`` (string|null): The name of the group.
    - ``is_open`` (bool): Is the group open?
    - ``candidates`` (list): List of all candidates on the group.
    - ``deadlines`` (list): List of all deadlines and deliveries on the group.
    - ``active_feedback`` (object|null): Information about the active feedback.
    - ``breadcrumbs`` (object): Contains id, long and shortnames of assignment, period and subject.
    """
    permissions = (IsAuthenticated, IsPublishedAndCandidate)
    resource = GroupResource

    def get_queryset(self):
        qry = super(AggregatedGroupInfo, self).get_queryset()
        qry = qry.select_related('feedback',
                                 'parentnode',
                                 'parentnode__parentnode',
                                 'parentnode__parentnode__parentnode')
        qry = qry.prefetch_related('deadlines',
                                   'deadlines__deliveries',
                                   'deadlines__deliveries__feedbacks',
                                   'deadlines__deliveries__filemetas',
                                   'examiners', 'examiners__user',
                                   'examiners__user__devilryuserprofile',
                                   'candidates', 'candidates__student',
                                   'candidates__student__devilryuserprofile')
        return qry
