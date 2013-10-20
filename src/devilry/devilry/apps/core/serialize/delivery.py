from django.core.urlresolvers import reverse

from devilry.utils.restformat import format_datetime
from devilry.utils.restformat import format_timedelta
from ..models import Delivery
from ..models import Candidate
from ..models import FileMeta
from .cache import serializedcache
from .filemeta import serialize_filemeta
from .candidate import serialize_candidate
from .candidate import serialize_candidate_anonymous
from .feedback import serialize_feedback
from .feedback import serialize_feedback_without_points



def _serialize_delivery(delivery, without_points=False, anonymous=False):
    serialize_candidate_function = serialize_candidate
    if anonymous:
        serialize_candidate_function = serialize_candidate_anonymous

    serialize_feedback_function = serialize_feedback
    if without_points:
        serialize_feedback_function = serialize_feedback_without_points

    timedelta_before_deadline = delivery.deadline.deadline - delivery.time_of_delivery
    delivered_by = None
    if delivery.delivered_by:
        delivered_by = serialize_candidate_function(delivery.delivered_by)
    return {'id': delivery.id,
            'number': delivery.number,
            'delivered_by': delivered_by,
            'after_deadline': delivery.after_deadline,
            'time_of_delivery': format_datetime(delivery.time_of_delivery),
            'offset_from_deadline': format_timedelta(timedelta_before_deadline),
            'alias_delivery': delivery.alias_delivery_id,
            'feedbacks': map(serialize_feedback_function, delivery.feedbacks.all()),
            'download_all_url': {'zip': reverse('devilry-delivery-download-all-zip',
                kwargs={'deliveryid': delivery.id})},
            'filemetas': map(serialize_filemeta, delivery.filemetas.all())}


def _serialize_delivery_without_points(delivery):
    return _serialize_delivery(delivery, without_points=True)

def _serialize_delivery_anonymous(delivery):
    return _serialize_delivery(delivery, anonymous=True)


for serializer in (_serialize_delivery, _serialize_delivery_without_points, _serialize_delivery_anonymous):
    serializedcache.add(serializer, {
        Delivery: None,
        FileMeta: lambda f: [f.delivery],
        Candidate: lambda c: [c.assignment_group.deliveries.all()],
    })


def serialize_delivery(delivery):
    return serializedcache.cache(_serialize_delivery, delivery)

def serialize_delivery_without_points(delivery):
    """
    Serialize without points. I.E.: For students.
    """
    serialized = serializedcache.cache(_serialize_delivery_without_points, delivery)
    return serialized

def serialize_delivery_anonymous(delivery):
    """
    Serialize with anonymousity maintained. I.E.: For examiners on anonymous assignments.
    """
    serialized = serializedcache.cache(_serialize_delivery_anonymous, delivery)
    return serialized
