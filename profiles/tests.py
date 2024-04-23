from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework.authtoken.models import Token


class ProfileTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user1', password='testpass')
        cls.other_user = User.objects.create_user(
            username='other', password='testpass')

        cls.profile = Profile.objects.get(owner=cls.user)
        cls.other_profile = Profile.objects.get(owner=cls.other_user)

        cls.user_token = Token.objects.create(user=cls.user)
        cls.other_user_token = Token.objects.create(user=cls.other_user)

    def authenticate(self, token):
        """
        Helper method to authenticate the test client
        with the specified user's token.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_auto_profile_creation(self):
        """
        Test automatic profile creation upon user registration.
        """
        new_user = User.objects.create_user(
            username='newuser', password='test123')
        self.assertIsNotNone(Profile.objects.get(
            owner=new_user), "Profile should be automatically created.")

    def test_list_profiles(self):
        """
        Ensure we can retrieve a list of all profiles.
        """
        url = reverse('profiles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_profile(self):
        """
        Ensure we can retrieve a single profile by id.
        """
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.profile.pk)

    def test_unauthorized_profile_update(self):
        """
        Ensure that a non-owner cannot update the profile.
        """
        self.authenticate(self.other_user_token)
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})
        data = {'name': 'Attempted Update'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
