from django.test import TestCase
from django.contrib.auth.models import User

from ...serialize.user import serialize_user



class TestSerializeUser(TestCase):
    def setUp(self):
        self.grandma = User.objects.create(
                username='grandma',
                email='grandma@example.com')
        profile = self.grandma.get_profile()
        profile.full_name = 'Elvira Grandma Coot'
        profile.save()

    def test_serialize_user(self):
        self.assertEquals(serialize_user(self.grandma), {
            'displayname': 'Elvira Grandma Coot',
            'email': 'grandma@example.com',
            'full_name': 'Elvira Grandma Coot',
            'id': 1,
            'username': 'grandma'})

    def test_serialize_user_no_fullname(self):
        profile = self.grandma.get_profile()
        profile.full_name = None
        profile.save()
        self.assertEquals(serialize_user(self.grandma), {
            'displayname': 'grandma',
            'email': 'grandma@example.com',
            'full_name': None,
            'id': 1,
            'username': 'grandma'})
