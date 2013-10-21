from datetime import datetime
from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.user import serialize_user
from ...serialize.candidate import serialize_candidate
from ...serialize.candidate import serialize_candidate_anonymous
from ...serialize.delivery import serialize_delivery
from ...serialize.deadline import serialize_deliveries
from ...serialize.group import serialize_deadlines
from ...serialize.group import serialize_tags
from ...serialize.group import serialize_examiners
from ...serialize.group import serialize_candidates
from ...serialize.group import serialize_candidates_anonymous


class TestSerializeGroup(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=["p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(candidate1):examiner(examiner1)"],
                 deadlines=['d1'])

        self.group = self.testhelper.sub_p1_a1_g1
        self.candidate1 = self.group.candidates.all()[0]
        self.deadline = self.testhelper.sub_p1_a1_g1_d1
        self.deadline.deadline = datetime(2013, 1, 2)
        self.deadline.save()

        self.delivery = self.testhelper.add_delivery("sub.p1.a1.g1", {"good.py": "print awesome"})
        self.delivery.time_of_delivery = datetime(2013, 1, 1)
        self.delivery.save(autoset_time_of_delivery=False, autoset_number=False)

    def test_serialize_deadlines(self):
        self.assertEquals(serialize_deadlines(self.group), [{
            'id': self.deadline.id,
            'deadline': '2013-01-02 00:00:00'
        }])

    def test_serialize_deadlines_with_deliveries(self):
        self.assertEquals(serialize_deadlines(self.group, with_deliveries=True), [{
            'id': self.deadline.id,
            'deadline': '2013-01-02 00:00:00',
            'deliveries': serialize_deliveries(self.deadline),
        }])

    def test_serialize_deadlines_with_deliveries_anonymous(self):
        self.assertEquals(serialize_deadlines(self.group, with_deliveries=True, anonymous=True), [{
            'id': self.deadline.id,
            'deadline': '2013-01-02 00:00:00',
            'deliveries': [serialize_delivery(self.delivery, anonymous=True)],
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

    def test_serialize_candidates(self):
        self.assertEquals(serialize_candidates(self.group), [serialize_candidate(self.candidate1)])

    def test_serialize_candidates_anonymous(self):
        self.assertEquals(serialize_candidates_anonymous(self.group),
                [serialize_candidate_anonymous(self.candidate1)])
