from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from devilry.utils.restformat import format_datetime
from devilry.utils.restformat import format_timedelta
from ..models import Delivery
from ..models import Candidate
from ..models import FileMeta
from ..models import StaticFeedback
from ..models.devilryuserprofile import DevilryUserProfile
from .cache import serializedcache
from .filemeta import serialize_filemeta
from .candidate import serialize_candidate
from .feedback import serialize_feedback



def _get_feedbacks(delivery):
    return delivery.feedbacks.all()

serializedcache.add(_get_feedbacks, {
    StaticFeedback: lambda feedback: [feedback.delivery]
})

def serialize_feedbacks(delivery, **serializefeedbackkwargs):
    feedbacks = serializedcache.cache(_get_feedbacks, delivery)
    return map(
            lambda feedback: serialize_feedback(feedback, **serializefeedbackkwargs),
            feedbacks)



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
            'download_all_url': {'zip': reverse('devilry-delivery-download-all-zip',
                kwargs={'deliveryid': delivery.id})},
            'filemetas': map(serialize_filemeta, delivery.filemetas.all())}


serializedcache.add(_serialize_delivery, {
    Delivery: None,
    FileMeta: lambda f: [f.delivery],
    Candidate: lambda c: Delivery.objects.filter(deadline__assignment_group=c.assignment_group),
    User: lambda u: Delivery.objects.filter(deadline__assignment_group__candidates__student=u),
    DevilryUserProfile: lambda p: Delivery.objects.filter(deadline__assignment_group__candidates__student=p.user)
})



def serialize_delivery(delivery, without_feedbacks=False, anonymous=False, without_points=False):
    serialized = serializedcache.cache(_serialize_delivery, delivery)
    if not without_feedbacks:
        serialized['feedbacks'] = serialize_feedbacks(delivery,
                without_points=without_points, anonymous=anonymous)
    if anonymous:
        if serialized['delivered_by']:
            del serialized['delivered_by']['user']
    return serialized
