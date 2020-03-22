from django.db import models
from django.contrib.auth.models import User


class Cat(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=30, blank=False)
    age = models.IntegerField(blank=False)

    def __str__(self):
        return self.name
