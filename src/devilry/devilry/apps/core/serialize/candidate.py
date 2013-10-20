from django.contrib.auth.models import User

from ..models import Candidate
from .cache import serializedcache
from .user import serialize_user



def _serialize_candidate(candidate):
    return {'id': candidate.id,
            'user': serialize_user(candidate.student),
            'candidate_id': candidate.candidate_id,
            'identifier': candidate.identifier}

serializedcache.add(_serialize_candidate, {
    Candidate: None,
    User: lambda u: Candidate.objects.filter(student=u)
})


def serialize_candidate(candidate):
    return serializedcache.cache(_serialize_candidate, candidate)

def serialize_candidate_anonymous(candidate):
    serialized = serializedcache.cache(_serialize_candidate, candidate)
    del serialized['user']
    return serialized
