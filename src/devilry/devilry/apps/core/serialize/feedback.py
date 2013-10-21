from devilry.utils.restformat import format_datetime
from .user import serialize_related_user


def serialize_feedback(feedback, anonymous=False, without_points=False):
    serialized = {'id': feedback.id,
            'rendered_view': feedback.rendered_view,
            'save_timestamp': format_datetime(feedback.save_timestamp),
            'grade': feedback.grade,
            'is_passing_grade': feedback.is_passing_grade,
            'delivery_id': feedback.delivery_id}
    if not anonymous:
        serialized['saved_by'] = serialize_related_user(feedback, 'saved_by', feedback.saved_by_id)
    if not without_points:
        serialized['points'] = feedback.points
    return serialized
