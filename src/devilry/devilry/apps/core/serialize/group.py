from ..models import Deadline
from .cache import serializedcache
from .deadline import serialize_deadline


def _serialize_deadlines(group):
    return map(serialize_deadline, group.deadlines.all())


serializedcache.add(_serialize_deadlines, {
    Deadline: lambda d: [d.assignment_group],
})


def serialize_deadlines(group):
    return serializedcache.cache(_serialize_deadlines, group)
