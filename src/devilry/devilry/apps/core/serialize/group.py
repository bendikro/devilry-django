from ..models import Deadline
from ..models import AssignmentGroupTag
from .cache import serializedcache
from .deadline import serialize_deadline
from .user import serialize_related_user
from .candidate import serialize_candidate
from .candidate import serialize_candidate_anonymous


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



def serialize_examiner(examiner):
    return {
            'id': examiner.id,
            'user': serialize_related_user(examiner, 'user', examiner.user_id)
    }

def _serialize_examiners(group):
    return map(serialize_examiner, group.examiners.all())

serializedcache.add(_serialize_examiners, {
    AssignmentGroupTag: lambda examiner: [examiner.assignment_group],
})



def _serialize_candidates(group):
    return map(serialize_candidate, group.candidates.all())

serializedcache.add(_serialize_candidates, {
    AssignmentGroupTag: lambda candidate: [candidate.assignment_group],
})

def _serialize_candidates_anonymous(group):
    return map(serialize_candidate_anonymous, group.candidates.all())

serializedcache.add(_serialize_candidates_anonymous, {
    AssignmentGroupTag: lambda candidate: [candidate.assignment_group],
})


def serialize_deadlines(group):
    return serializedcache.cache(_serialize_deadlines, group)

def serialize_tags(group):
    return serializedcache.cache(_serialize_tags, group)

def serialize_examiners(group):
    return serializedcache.cache(_serialize_examiners, group)

def serialize_candidates(group):
    return serializedcache.cache(_serialize_candidates, group)

def serialize_candidates_anonymous(group):
    """
    Serialize candidates without any data that breaks the anonymity of the candidate.
    """
    return serializedcache.cache(_serialize_candidates_anonymous, group)
