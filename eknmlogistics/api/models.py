import random
import string

from django.db import models


def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class User(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    password_hash = models.CharField(max_length=32)
    token = models.CharField(max_length=32, default=randomString(32))

    def resetToken(self):
        token = randomString(32)

    def __str__(self):
        return self.name
