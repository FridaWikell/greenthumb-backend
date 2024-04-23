from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """

    HARDINESS_ZONES = (
        (0, 'Not applicable'),
        (1, 'Zone 1'),
        (2, 'Zone 2'),
        (3, 'Zone 3'),
        (4, 'Zone 4'),
        (5, 'Zone 5'),
        (6, 'Zone 6'),
        (7, 'Zone 7'),
        (8, 'Zone 8'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default-image_r3k7wr', blank=True
    )
    hardiness_zone = models.IntegerField(choices=HARDINESS_ZONES, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
