from django.contrib.auth.models import User
from django.db import models

class Feed(models.Model):
    url = models.CharField(max_length=1000, unique=True)
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
