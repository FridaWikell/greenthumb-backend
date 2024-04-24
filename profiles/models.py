from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


"""
Code based at https://github.com/Code-Institute-Solutions/drf-api
"""
class Profile(models.Model):
    """
    Represents a user profile linked to a Django User model.
    The profiles are ordered by the date of creation,
    with the most recently created profiles appearing first.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../profile_default'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a Profile instance automatically whenever
    a new User instance is created. A profile is only created if a new User
    instance ('created' is True) is saved, ensuring that existing users
    do not get multiple profiles.
    """
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
