from datetime import datetime
from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.candidate import serialize_candidate
from ...serialize.candidate import serialize_candidate_anonymous
from ...serialize.feedback import serialize_feedback
from ...serialize.filemeta import serialize_filemeta
from ...serialize.delivery import serialize_delivery


class TestSerializeDelivery(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=["p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(student1):examiner(examiner1)"],
                 deadlines=['d1'])

        deadline = self.testhelper.sub_p1_a1_g1_d1
        deadline.deadline = datetime(2013, 1, 2)
        deadline.save()

        self.delivery = self.testhelper.add_delivery("sub.p1.a1.g1", {"good.py": "print awesome"})
        self.delivery.time_of_delivery = datetime(2013, 1, 1)
        self.delivery.save(autoset_time_of_delivery=False, autoset_number=False)

        self.feedback = self.testhelper.add_feedback(self.delivery,
                verdict={"grade": "C", "points": 85, "is_passing_grade": True})
        self.feedback.save_timestamp = datetime(2013, 3, 1)
        self.feedback.save(autoset_timestamp_to_now=False)
        self.filemeta = self.delivery.filemetas.all()[0]
        self.candidate = self.testhelper.sub_p1_a1_g1.candidates.all()[0]

    def test_serialize(self):
        self.assertEquals(serialize_delivery(self.delivery), {
            'id': 1,
            'after_deadline': False,
            'alias_delivery': None,
            'number': 1,
            'time_of_delivery': '2013-01-01 00:00:00',
            'download_all_url': {
                'zip': '/student/show-delivery/compressedfiledownload/{}'.format(self.delivery.id)
            },
            'offset_from_deadline': {'days': 1, 'hours': 0, 'minutes': 0, 'seconds': 0},
            'delivered_by': serialize_candidate(self.candidate),
            'feedbacks': [serialize_feedback(self.feedback)],
            'filemetas': [serialize_filemeta(self.filemeta)],
        })

    def test_serialize_without_points(self):
        self.assertEquals(serialize_delivery(self.delivery, without_points=True), {
            'id': 1,
            'after_deadline': False,
            'alias_delivery': None,
            'number': 1,
            'time_of_delivery': '2013-01-01 00:00:00',
            'download_all_url': {
                'zip': '/student/show-delivery/compressedfiledownload/{}'.format(self.delivery.id)
            },
            'offset_from_deadline': {'days': 1, 'hours': 0, 'minutes': 0, 'seconds': 0},
            'delivered_by': serialize_candidate(self.candidate),
            'feedbacks': [serialize_feedback(self.feedback, without_points=True)],
            'filemetas': [serialize_filemeta(self.filemeta)],
        })

    def test_serialize_anonymous(self):
        self.assertEquals(serialize_delivery(self.delivery, anonymous=True), {
            'id': 1,
            'after_deadline': False,
            'alias_delivery': None,
            'number': 1,
            'time_of_delivery': '2013-01-01 00:00:00',
            'download_all_url': {
                'zip': '/student/show-delivery/compressedfiledownload/{}'.format(self.delivery.id)
            },
            'offset_from_deadline': {'days': 1, 'hours': 0, 'minutes': 0, 'seconds': 0},
            'delivered_by': serialize_candidate_anonymous(self.candidate),
            'feedbacks': [serialize_feedback(self.feedback, anonymous=True)],
            'filemetas': [serialize_filemeta(self.filemeta)],
        })
