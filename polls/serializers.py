from rest_framework import serializers
from .models import Question, Answer, Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'answer', 'voter', 'created_at']
        # read_only_fields = ('voter',)

    def validate(self, data):
        # More defensive approach with checks
        question = data['answer'].question
        voter = self.context['request'].user
        if Vote.objects.filter(answer__question=question, voter=voter).exists():
            raise serializers.ValidationError("You have already voted on this question.")
        return data


class AnswerSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'created_at', 'votes_count']

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username')
    answers = AnswerSerializer(many=True, read_only=False, required=False)
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'owner', 'owner_username', 'text', 'created_at', 'answers', 'votes_count']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question