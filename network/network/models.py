from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(blank=False,)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.post


class Movie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name




