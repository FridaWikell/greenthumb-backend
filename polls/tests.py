from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Question, Answer, Vote


class QAVTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the entire test class
        """
        cls.user = User.objects.create_user(
            username='user', password='testpass')
        cls.other_user = User.objects.create_user(
            username='other', password='testpass')

        cls.question = Question.objects.create(
            owner=cls.user,
            text="What is the airspeed velocity of an unladen swallow?"
        )

        cls.answer = Answer.objects.create(
            question=cls.question,
            text="African or European swallow?"
        )

        cls.vote = Vote.objects.create(
            answer=cls.answer,
            voter=cls.user,
            question=cls.question
        )

    def test_list_questions(self):
        """
        Test retrieving a list of questions.
        """
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_question_authenticated(self):
        """
        Test creating a question by an authenticated user.
        """
        self.client.login(username='user', password='testpass')
        url = reverse('question-list')
        data = {'text': 'How many roads must a man walk down?'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_retrieve_question_detail(self):
        """
        Test retrieving a specific question.
        """
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question.id)

    def test_delete_question_owner(self):
        """
        Test deleting a question by the owner.
        """
        self.client.login(username='user', password='testpass')
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())

    def test_list_answers(self):
        """
        Test retrieving a list of answers.
        """
        url = reverse('answer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_vote_authenticated(self):
        """
        Ensure that an authenticated user can create a vote.
        """
        self.client.login(username='other', password='testpass')
        url = reverse('vote-list')
        Vote.objects.filter(
            voter=self.other_user, question=self.question).delete()
        data = {'answer': self.answer.id}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Vote.objects.filter(voter=self.other_user).count(), 1)

    def test_vote_duplicate_prevention(self):
        """
        Test prevention of duplicate votes
        on the same question by the same user.
        """
        self.client.login(username='user', password='testpass')
        url = reverse('vote-list')
        data = {'answer': self.answer.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
