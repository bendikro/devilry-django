from django.test import TestCase

from ...testhelper import TestHelper
from ...serialize.filemeta import serialize_filemeta

class TestSerializeFileMeta(TestCase):

    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni",
                 subjects=["sub"],
                 periods=["p1:admin(teacher1):begins(-1):ends(5)"],
                 assignments=["a1"],
                 assignmentgroups=["g1:candidate(student1):examiner(examiner1)"],
                 deadlines=['d1'])
        goodFile = {"good.py": "print awesome"}
        delivery = self.testhelper.add_delivery("sub.p1.a1.g1", goodFile)
        self.filemeta = delivery.add_file('hello.txt', ['hello world'])

    def test_serialize(self):
        self.assertEquals(serialize_filemeta(self.filemeta), {
            'download_url': '/student/show-delivery/filedownload/2',
            'filename': 'hello.txt',
            'id': self.filemeta.id,
            'pretty_size': '11 bytes',
            'size': 11})
