from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from followers.models import Follower


class FollowerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for the entire class"""
        cls.user = User.objects.create_user(username='user', password='pass')
        cls.other_user = User.objects.create_user(
            username='other', password='pass')
        cls.follower = Follower.objects.create(
            owner=cls.user, followed=cls.other_user)

    def test_list_followers(self):
        """
        Ensure we can retrieve a list of all followers.
        This test verifies that the list view returns a successful response
        and that the response content is a list within a paginated structure.
        """
        url = reverse('follower-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_follower_authenticated(self):
        """
        Ensure that an authenticated user can follow another user. This tests
        the creation of a Follower instance by an authenticated user.
        """
        self.client.login(username='other', password='pass')
        url = reverse('follower-list')
        data = {'owner': self.other_user.id, 'followed': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follower.objects.count(), 2)

    def test_create_follower_unauthenticated(self):
        """
        Ensure that unauthenticated users cannot follow others. Tests that
        the API properly restricts this action to authenticated users only.
        """
        url = reverse('follower-list')
        data = {'owner': self.user.id, 'followed': self.other_user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_follower_detail(self):
        """
        Test retrieving a single follower instance.
        Ensures that the detail view returns the correct follower data.
        """
        url = reverse('follower-detail', kwargs={'pk': self.follower.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.follower.id)

    def test_unfollow_follower_owner(self):
        """
        Ensure the owner of a follow relationship can terminate it by
        unfollowing. This tests the destroy method in the view for
        a Follower instance.
        """
        self.client.login(username='user', password='pass')
        url = reverse('follower-detail', kwargs={'pk': self.follower.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follower.objects.filter(id=self.follower.id).exists())

    def test_unfollow_follower_not_owner(self):
        """
        Ensure that users who do not own a follow relationship cannot
        terminate it. Verifies proper permission handling by ensuring
        non-owners cannot unfollow.
        """
        self.client.login(username='other', password='pass')
        url = reverse('follower-detail', kwargs={'pk': self.follower.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Follower.objects.filter(id=self.follower.id).exists())
