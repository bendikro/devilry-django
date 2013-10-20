from datetime import datetime
from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.feedback import serialize_feedback
from ...serialize.feedback import serialize_feedback_without_points

class TestSerializeFeedback(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=[
                          "p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(student1):examiner(examiner1)"],
                 deadlines=['d1'])
        self.goodFile = {"good.py": "print awesome"}
        self.okVerdict = {"grade": "C", "points": 85, "is_passing_grade": True}
        self.delivery = self.testhelper.add_delivery("sub.p1.a1.g1", self.goodFile)
        self.feedback = self.testhelper.add_feedback(self.delivery, verdict=self.okVerdict)
        self.feedback.save_timestamp = datetime(2013, 1, 1)
        self.feedback.save(autoset_timestamp_to_now=False)

    def test_serialize(self):
        self.assertEquals(serialize_feedback(self.feedback), {
            'grade': 'C',
            'id': self.feedback.id,
            'is_passing_grade': True,
            'points': 85,
            'rendered_view': 'This is a default static feedback',
            'save_timestamp': '2013-01-01 00:00:00'})

    def test_serialize_without_points(self):
        self.assertEquals(serialize_feedback_without_points(self.feedback), {
            'grade': 'C',
            'id': self.feedback.id,
            'is_passing_grade': True,
            'rendered_view': 'This is a default static feedback',
            'save_timestamp': '2013-01-01 00:00:00'})
