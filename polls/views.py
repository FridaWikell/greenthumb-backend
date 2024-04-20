from django.db.models import Count
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import ValidationError
from .models import Question, Answer, Vote
from .serializers import QuestionSerializer, AnswerSerializer, VoteSerializer
from greenthumb.permissions import IsOwnerOrReadOnly


# Questions
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.annotate(
        votes_count=Count('answers__votes', distinct=True)).order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Ensure users are authenticated to create questions
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'owner__username',
        'text',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.annotate(
        votes_count=Count('answers__votes', distinct=True)).order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Custom permission to check the owner

# Answers
class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.objects.annotate(
        votes_count=Count('votes', distinct=True)  # Correctly count votes directly related to answers
    ).order_by('-created_at')
    serializer_class = AnswerSerializer

class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.annotate(
        votes_count=Count('votes', distinct=True)  # Correctly count votes directly related to answers
    ).order_by('-created_at')
    serializer_class = AnswerSerializer

# Votes
class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        # Retrieve the question associated with the answer to ensure user hasn't voted already
        question = serializer.validated_data['answer'].question

        if Vote.objects.filter(answer__question=question, voter=user).exists():
            raise ValidationError({"error": "You have already voted on this question"})

        serializer.save(voter=user)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
