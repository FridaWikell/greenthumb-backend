from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Comment, Post


class CommentTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the entire TestClass
        """
        cls.user = User.objects.create_user(username='user', password='pass')
        cls.other_user = User.objects.create_user(
            username='other', password='pass')
        cls.post = Post.objects.create(
            title="A Post", content="Some content here", owner=cls.user)
        cls.comment = Comment.objects.create(
            content="A Comment", owner=cls.user, post=cls.post)

    def test_list_comments(self):
        """
        Test retrieving a list of comments. This test ensures that
        the list endpoint returns a successful HTTP 200 response
        and that the response content is a list.
        """
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertTrue(isinstance(response.data['results'], list))
        self.assertEqual(len(response.data['results']), 1)

    def test_create_comment_authenticated(self):
        """
        Test the creation of a comment by an authenticated user.
        This test ensures that authenticated users can post comments and that
        posting successfully increases the count of comments.
        """
        self.client.login(username='user', password='pass')
        url = reverse('comment-list')
        data = {'content': 'New Comment', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_comment_unauthenticated(self):
        """
        Test that unauthenticated users cannot create comments.
        This checks that the API properly restricts comment
        creation to authenticated users.
        """
        url = reverse('comment-list')
        data = {'content': 'New Comment', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_comment(self):
        """
        Test retrieving a single comment by its ID.
        This test ensures that the detail view returns
        a correct comment object based on its ID.
        """
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment.id)

    def test_update_comment_owner(self):
        """
        Test that the owner of a comment can update it.
        This test verifies that proper permissions
        are enforced and that the update functionality works.
        """
        self.client.login(username='user', password='pass')
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        data = {'content': 'Updated Comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated Comment')

    def test_delete_comment_owner(self):
        """
        Test that the owner of a comment can delete it.
        This ensures that delete permissions are correctly
        enforced and the comment is properly removed.
        """
        self.client.login(username='user', password='pass')
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.exists())

    def test_update_comment_not_owner(self):
        """
        Test that a user who does not own a comment cannot update it.
        This checks the permission system to ensure that users cannot
        alter other users' comments.
        """
        self.client.login(username='other', password='pass')
        url = reverse('comment-detail', kwargs={'pk': self.comment.id})
        data = {'content': 'Illegal Update'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
