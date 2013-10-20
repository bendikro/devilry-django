from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.candidate import serialize_cadidate
from ...serialize.user import serialize_user

class TestSerializeCandidate(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=["p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(student1)"])
        self.candidate = self.testhelper.sub_p1_a1_g1.candidates.all()[0]

    def test_serialize(self):
        serialized = serialize_cadidate(self.candidate)
        self.assertEquals(serialized, {
            'candidate_id': None,
            'id': 1,
            'identifier': u'student1',
            'user': serialize_user(self.candidate.student)})
