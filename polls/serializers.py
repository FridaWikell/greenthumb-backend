from rest_framework import serializers
from .models import Question, Answer, Vote


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source='voter.username')  # Assuming you want to display the username

    class Meta:
        model = Vote
        fields = ['id', 'answer', 'voter', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = AnswerSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Question
        fields = ['id', 'owner', 'text', 'created_at', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question