from devilry.utils.restformat import format_datetime
from ..models import Delivery
from .cache import serializedcache
from .delivery import serialize_delivery
from .delivery import serialize_delivery_without_points
from .delivery import serialize_delivery_anonymous
from .delivery import serialize_delivery_without_points_anonymous


def serialize_deadline(deadline):
    return {'id': deadline.id,
            'deadline': format_datetime(deadline.deadline)}


def _serialize_deliveries(deadline):
    return list(deadline.deliveries.filter(successful=True))

serializedcache.add(_serialize_deliveries, {
    Delivery: lambda delivery: [delivery.deadline],
})

def _get_deliveries(deadline):
    return serializedcache.cache(_serialize_deliveries, deadline)

def serialize_deliveries(deadline):
    return map(serialize_delivery, _get_deliveries(deadline))


def serialize_deliveries_without_points(deadline):
    """
    Serialize without points. I.E.: For students on non-anonymous assignments.
    """
    return map(serialize_delivery_without_points, _get_deliveries(deadline))

def serialize_deliveries_anonymous(deadline):
    """
    Serialize with anonymousity maintained. I.E.: For examiners on anonymous assignments.
    """
    return map(serialize_delivery_anonymous, _get_deliveries(deadline))

def serialize_deliveries_without_points_anonymous(deadline):
    """
    Serialize with anonymousity maintained. I.E.: For students on anonymous assignments.
    """
    return map(serialize_delivery_without_points_anonymous, _get_deliveries(deadline))
