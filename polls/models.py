from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Orders by the creation time by default

    def __str__(self):
        return f"Question {self.id} by {self.owner}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer {self.id} to Question {self.question.id}"

class Vote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # This is new
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'voter')  # Enforce one vote per question per user
        ordering = ['-created_at']

    def __str__(self):
        return f"Vote by {self.voter} for {self.answer}"
