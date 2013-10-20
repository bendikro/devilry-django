def serialize_user(user):
    return {'email': user.email,
            'username': user.username,
            'id': user.id,
            'full_name': user.get_profile().full_name,
            'displayname': user.get_profile().full_name or user.username}
