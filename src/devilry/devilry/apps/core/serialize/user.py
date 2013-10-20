from django.contrib.auth.models import User

from ..models.devilryuserprofile import DevilryUserProfile
from .cache import serializedcache



def _serialize_user(user):
    return {'email': user.email,
            'username': user.username,
            'id': user.id,
            'full_name': user.get_profile().full_name,
            'displayname': user.get_profile().full_name or user.username}

serializedcache.add(_serialize_user, {
    User: None,
    DevilryUserProfile: lambda p: [p.user]
})


def serialize_user(user):
    return serializedcache.cache(_serialize_user, user)

def serialize_related_user(obj, attribute, user_id):
    return serializedcache.cache_related(_serialize_user, obj, attribute, user_id)
