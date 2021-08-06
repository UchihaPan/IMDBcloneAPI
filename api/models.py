from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class platform(models.Model):
    name = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    website = models.URLField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey('platform', on_delete=models.CASCADE, related_name='movies')
    average_rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name + ' ' )


class Review(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')

    def __str__(self):
        return str(self.review_rating) + ' | ' + self.movie.name
