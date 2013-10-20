from devilry.utils.restformat import format_datetime
from .user import serialize_user


def serialize_feedback(feedback):
    return {'id': feedback.id,
            'rendered_view': feedback.rendered_view,
            'save_timestamp': format_datetime(feedback.save_timestamp),
            'grade': feedback.grade,
            'is_passing_grade': feedback.is_passing_grade,
            'delivery_id': feedback.delivery.id,
            'saved_by': serialize_user(feedback.saved_by),
            'points': feedback.points}


def serialize_feedback_without_points(feedback):
    serialized = serialize_feedback(feedback)
    del serialized['points']
    return serialized

def serialize_feedback_anonymous(feedback):
    serialized = serialize_feedback(feedback)
    del serialized['saved_by']
    return serialized
