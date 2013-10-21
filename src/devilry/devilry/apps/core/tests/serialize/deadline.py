from datetime import datetime
from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.delivery import serialize_delivery
from ...serialize.deadline import serialize_deadline
from ...serialize.deadline import serialize_deliveries


class TestSerializeDeadline(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=["p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(student1):examiner(examiner1)"],
                 deadlines=['d1'])

        self.deadline = self.testhelper.sub_p1_a1_g1_d1
        self.deadline.deadline = datetime(2013, 1, 2)
        self.deadline.save()

        self.delivery = self.testhelper.add_delivery("sub.p1.a1.g1", {"good.py": "print awesome"})
        self.delivery.time_of_delivery = datetime(2013, 1, 1)
        self.delivery.save(autoset_time_of_delivery=False, autoset_number=False)

        self.feedback = self.testhelper.add_feedback(self.delivery,
                verdict={"grade": "C", "points": 85, "is_passing_grade": True})
        self.feedback.save_timestamp = datetime(2013, 3, 1)
        self.feedback.save(autoset_timestamp_to_now=False)
        self.filemeta = self.delivery.filemetas.all()[0]
        self.candidate = self.testhelper.sub_p1_a1_g1.candidates.all()[0]

    def test_serialize_deadline(self):
        self.assertEquals(serialize_deadline(self.deadline), {
            'id': self.deadline.id,
            'deadline': '2013-01-02 00:00:00'
        })

    def test_serialize_deadline_with_deliveries(self):
        self.assertEquals(serialize_deadline(self.deadline, with_deliveries=True), {
            'id': self.deadline.id,
            'deadline': '2013-01-02 00:00:00',
            'deliveries': serialize_deliveries(self.delivery)
        })

    def test_serialize_deliveries(self):
        self.assertEquals(serialize_deliveries(self.deadline),
                [serialize_delivery(self.delivery)])

    def test_serialize_deliveries_without_points_anonymous(self):
        self.assertEquals(serialize_deliveries(self.deadline, anonymous=True, without_points=True),
                [serialize_delivery(self.delivery, anonymous=True, without_points=True)])
