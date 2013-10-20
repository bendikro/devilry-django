from devilry.utils.restformat import format_datetime


def serialize_deadline(deadline):
    return {'id': deadline.id,
            'deadline': format_datetime(deadline.deadline)}
