from devilry.utils.restformat import format_datetime
from .cache import serializedcache
from ..models import StaticFeedback



def _serialize_feedback(feedback):
    return {'id': feedback.id,
            'rendered_view': feedback.rendered_view,
            'save_timestamp': format_datetime(feedback.save_timestamp),
            'grade': feedback.grade,
            'is_passing_grade': feedback.is_passing_grade,
            'points': feedback.points}

serializedcache.add(_serialize_feedback, {
    StaticFeedback: None
})


def serialize_feedback(feedback):
    return serializedcache.cache(_serialize_feedback, feedback)

def serialize_feedback_without_points(feedback):
    serialized = serializedcache.cache(_serialize_feedback, feedback)
    del serialized['points']
    return serialized
