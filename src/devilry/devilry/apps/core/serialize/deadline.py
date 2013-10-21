from devilry.utils.restformat import format_datetime
from ..models import Delivery
from .cache import serializedcache
from .delivery import serialize_delivery


def _serialize_deliveries(deadline):
    return list(deadline.deliveries.filter(successful=True))

serializedcache.add(_serialize_deliveries, {
    Delivery: lambda delivery: [delivery.deadline],
})

def _get_deliveries(deadline):
    return serializedcache.cache(_serialize_deliveries, deadline)


def serialize_deliveries(deadline, **deliveryserializerkwargs):
    return map(
            lambda delivery: serialize_delivery(delivery, **deliveryserializerkwargs),
            _get_deliveries(deadline))

def serialize_deadline(deadline, with_deliveries=False, **deliveryserializerkwargs):
    serialized = {
            'id': deadline.id,
            'deadline': format_datetime(deadline.deadline)}
    if with_deliveries:
        serialized['deliveries'] = serialize_deliveries(deadline, **deliveryserializerkwargs)
    return serialized
