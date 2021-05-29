"""
Auto Generated test
You may need to change some parts
"""
from rest_framework.test import APITestCase
from django_seed import Seed

from api.models import *

seeder = Seed.seeder()


class ApiModelTest(APITestCase):
    """
    api Model Test
    Auto Generated
    """

    def setUp(self) -> None:
        pass

    def test_user_model(self):
        seeder.add_entity(User, 1)
        seeder.execute()
        self.assertTrue(User.objects.exists())

    def test_profile_model_signal(self):
        seeder.add_entity(User, 1)
        seeder.execute()
        self.assertTrue(User.objects.exists())
        self.assertTrue(Profile.objects.exists())
        first_object = User.objects.first()
        second_object = Profile.objects.first()
        self.assertEqual(second_object.user, first_object)
