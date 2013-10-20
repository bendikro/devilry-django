from ..models import Deadline
from ..models import AssignmentGroupTag
from .cache import serializedcache
from .deadline import serialize_deadline


def _serialize_deadlines(group):
    return map(serialize_deadline, group.deadlines.all())

serializedcache.add(_serialize_deadlines, {
    Deadline: lambda d: [d.assignment_group],
})


def serialize_tag(tag):
    return {'id': tag.id,
            'tag': tag.tag}

def _serialize_tags(group):
    return map(serialize_tag, group.tags.all())

serializedcache.add(_serialize_tags, {
    AssignmentGroupTag: lambda tag: [tag.assignment_group],
})


def serialize_deadlines(group):
    return serializedcache.cache(_serialize_deadlines, group)

def serialize_tags(group):
    return serializedcache.cache(_serialize_tags, group)
