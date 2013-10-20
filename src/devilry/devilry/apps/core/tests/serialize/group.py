from datetime import datetime
from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.user import serialize_user
from ...serialize.group import serialize_deadlines
from ...serialize.group import serialize_tags
from ...serialize.group import serialize_examiners


class TestSerializeGroup(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=["p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(student1):examiner(examiner1)"],
                 deadlines=['d1'])

        self.group = self.testhelper.sub_p1_a1_g1
        self.deadline = self.testhelper.sub_p1_a1_g1_d1
        self.deadline.deadline = datetime(2013, 1, 2)
        self.deadline.save()

    def test_serialize_deadlines(self):
        self.assertEquals(serialize_deadlines(self.group), [{
            'id': self.deadline.id,
            'deadline': '2013-01-02 00:00:00'
        }])

    def test_serialize_tags(self):
        a = self.group.tags.create(tag='a')
        b = self.group.tags.create(tag='b')
        self.assertEquals(serialize_tags(self.group), [{
            'id': a.id,
            'tag': 'a'
        }, {
            'id': b.id,
            'tag': 'b'
        }])

    def test_serialize_examiners(self):
        examiner1 = self.group.examiners.all()[0]
        self.assertEquals(serialize_examiners(self.group), [{
            'id': examiner1.id,
            'user': serialize_user(examiner1.user)
        }])
