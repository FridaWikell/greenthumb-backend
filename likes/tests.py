from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from posts.models import Post
from likes.models import Like


class LikeTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for the entire class"""
        cls.user = User.objects.create_user(username='user', password='pass')
        cls.other_user = User.objects.create_user(
            username='other', password='pass')
        cls.post = Post.objects.create(
            title="A Post", content="Some content", owner=cls.user)
        cls.like = Like.objects.create(owner=cls.user, post=cls.post)

    def test_list_likes(self):
        """
        Ensure we can retrieve a list of all likes.
        """
        url = reverse('likes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_like_authenticated(self):
        """
        Ensure that an authenticated user can like a post.
        """
        self.client.login(username='other', password='pass')
        url = reverse('likes-list')
        data = {'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 2)

    def test_create_like_unauthenticated(self):
        """
        Ensure that unauthenticated users cannot create likes.
        """
        url = reverse('likes-list')
        data = {'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_like(self):
        """
        Test retrieving a single like instance.
        """
        url = reverse('likes-detail', kwargs={'pk': self.like.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.like.id)

    def test_delete_like_owner(self):
        """
        Ensure the owner of a like can delete it.
        """
        self.client.login(username='user', password='pass')
        url = reverse('likes-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(id=self.like.id).exists())

    def test_delete_like_not_owner(self):
        """
        Ensure that users who do not own a like cannot delete it.
        """
        self.client.login(username='other', password='pass')
        url = reverse('likes-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Like.objects.filter(id=self.like.id).exists())
