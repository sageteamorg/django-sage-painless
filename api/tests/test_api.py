"""
Auto Generated test
You may need to change some parts
"""
from django.urls import reverse
from rest_framework.test import APITestCase
from django_seed import Seed

from api.models import *

seeder = Seed.seeder()


class ApiAPITest(APITestCase):
    """
    api API Test
    Auto Generated
    """

    def setUp(self) -> None:

        seeder.add_entity(User, 3)

        seeder.execute()  # create instances

    def test_user_list_success(self):
        """
        test User list
        """
        url = reverse('user-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if response.data.get('count'):
            self.assertGreater(response.data['count'], 0)
        self.assertGreater(len(response.data), 0)

    def test_user_detail_success(self):
        """
        test User detail
        """
        user = User.objects.first()
        url = reverse('user-detail', args=[user.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('username'), user.username)

        self.assertEqual(response.data.get('password'), user.password)

        self.assertEqual(response.data.get('first_name'), user.first_name)

        self.assertEqual(response.data.get('last_name'), user.last_name)

        self.assertEqual(response.data.get('is_active'), user.is_active)

    def test_profile_list_success(self):
        """
        test Profile list
        """
        url = reverse('profile-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if response.data.get('count'):
            self.assertGreater(response.data['count'], 0)
        self.assertGreater(len(response.data), 0)

    def test_profile_detail_success(self):
        """
        test Profile detail
        """
        profile = Profile.objects.first()
        url = reverse('profile-detail', args=[profile.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('description'), profile.description)
