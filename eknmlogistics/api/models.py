from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    password_hash = models.CharField(max_length=32)

    def __str__(self):
        return self.name
