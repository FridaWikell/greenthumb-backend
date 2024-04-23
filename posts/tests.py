from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post
from likes.models import Like
import tempfile
from PIL import Image


class PostTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create user accounts and a sample post with a temporary image
        for use in all test methods.
        """
        cls.user = User.objects.create_user(
            username='user', password='testpass')
        cls.other_user = User.objects.create_user(
            username='other', password='testpass')

        cls.post = Post.objects.create(
            owner=cls.user,
            title="First Post",
            content="This is the first post",
            hardiness_zone='5'
        )

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        cls.image = tmp_file

    def tearDown(cls):
        """
        Close and remove the temporary image file after tests.
        """
        cls.image.close()

    def test_list_posts(self):
        """
        Test retrieving a list of posts.
        """
        url = reverse('posts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_post_authenticated(self):
        """
        Ensure that an authenticated user can create a post.
        """
        self.client.login(username='user', password='testpass')
        url = reverse('posts-list')
        data = {
            'title': 'New Post',
            'content': 'Content of the new post',
            'image': self.image,
            'hardiness_zone': '3'
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(response.data['owner'], 'user')

    def test_retrieve_update_delete_post(self):
        """
        Ensure retrieve, update and delete operations are correctly handled.
        """
        self.client.login(username='user', password='testpass')
        url = reverse('post-detail', kwargs={'pk': self.post.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_data = {'title': 'Updated Title'}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_unauthorized_access(self):
        """
        Ensure unauthorized users cannot update or delete posts.
        """
        self.client.login(username='other', password='testpass')
        url = reverse('post-detail', kwargs={'pk': self.post.pk})

        update_data = {'title': 'Illegally Updated Title'}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
