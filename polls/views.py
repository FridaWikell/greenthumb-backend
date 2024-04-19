from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer, Vote
from .serializers import QuestionSerializer, AnswerSerializer, VoteSerializer
from greenthumb.permissions import IsOwnerOrReadOnly


# Questions
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]  # Ensure users are authenticated to create questions

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Custom permission to check the owner

# Answers
class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

# Votes
class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Retrieve the current user
        user = self.request.user
        # Retrieve the question associated with the answer to ensure user hasn't voted already
        question = serializer.validated_data['answer'].question

        # Check if the user has already voted on this question
        if Vote.objects.filter(answer__question=question, voter=user).exists():
            # If the user has already voted, return an error response
            raise serializers.ValidationError({"error": "You have already voted on this question"})
        else:
            # If not, save the vote with the current user set as the voter
            serializer.save(voter=user)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
