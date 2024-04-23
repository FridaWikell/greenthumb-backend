from django.db.models import Count
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import ValidationError
from .models import Question, Answer, Vote
from .serializers import QuestionSerializer, AnswerSerializer, VoteSerializer
from greenthumb.permissions import IsOwnerOrReadOnly


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
    permission_classes = [IsOwnerOrReadOnly]


class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.objects.annotate(votes_count=Count('votes', distinct=True)).order_by('-created_at')
    serializer_class = AnswerSerializer


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.annotate(votes_count=Count('votes', distinct=True))
    serializer_class = AnswerSerializer


class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        question = serializer.validated_data['answer'].question

        if Vote.objects.filter(answer__question=question, voter=user).exists():
            raise ValidationError({"error": "You have already voted on this question"})

        serializer.save(voter=user, question=question)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
