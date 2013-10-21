from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from devilry.utils.restformat import format_datetime
from devilry.utils.restformat import format_timedelta
from ..models import Delivery
from ..models import Candidate
from ..models import FileMeta
from ..models.devilryuserprofile import DevilryUserProfile
from .cache import serializedcache
from .filemeta import serialize_filemeta
from .candidate import serialize_candidate
from .feedback import serialize_feedback



def _serialize_delivery(delivery):
    timedelta_before_deadline = delivery.deadline.deadline - delivery.time_of_delivery
    delivered_by = None
    if delivery.delivered_by:
        delivered_by = serialize_candidate(delivery.delivered_by)
    return {'id': delivery.id,
            'number': delivery.number,
            'delivered_by': delivered_by,
            'after_deadline': delivery.after_deadline,
            'time_of_delivery': format_datetime(delivery.time_of_delivery),
            'offset_from_deadline': format_timedelta(timedelta_before_deadline),
            'alias_delivery': delivery.alias_delivery_id,
            'feedbacks': map(serialize_feedback, delivery.feedbacks.all()),
            'download_all_url': {'zip': reverse('devilry-delivery-download-all-zip',
                kwargs={'deliveryid': delivery.id})},
            'filemetas': map(serialize_filemeta, delivery.filemetas.all())}


def _serialize_delivery_anonymous(delivery):
    return _serialize_delivery(delivery, anonymous=True)


for serializer in (_serialize_delivery, _serialize_delivery_anonymous):
    serializedcache.add(serializer, {
        Delivery: None,
        FileMeta: lambda f: [f.delivery],
        Candidate: lambda c: [Delivery.objects.filter(deadline__assignment_group=c.assignment_group)],
        User: lambda u: [Delivery.objects.filter(deadline__assignment_group__candidates__student=u)],
        DevilryUserProfile: lambda p: [Delivery.objects.filter(deadline__assignment_group__candidates__student=p.user)]
    })



def serialize_delivery(delivery, anonymous=False, without_points=False):
    serialized = serializedcache.cache(_serialize_delivery, delivery)
    if without_points or anonymous:
        for feedback in serialized['feedbacks']:
            if without_points:
                del feedback['points']
            if anonymous:
                del feedback['saved_by']
    if anonymous:
        if serialized['delivered_by']:
            del serialized['delivered_by']['user']
    return serialized


def serialize_delivery_without_points(delivery):
    """
    Serialize without points. I.E.: For students on non-anonymous assignments.
    """
    return serialize_delivery(delivery, without_points=True)

def serialize_delivery_anonymous(delivery):
    """
    Serialize with anonymousity maintained. I.E.: For examiners on anonymous assignments.
    """
    return serialize_delivery(delivery, anonymous=True)

def serialize_delivery_without_points_anonymous(delivery):
    """
    Serialize with anonymousity maintained. I.E.: For students on anonymous assignments.
    """
    return serialize_delivery(delivery, anonymous=True, without_points=True)
