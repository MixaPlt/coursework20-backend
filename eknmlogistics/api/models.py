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


payment_images = [
    'https://upload.wikimedia.org/wikipedia/commons/7/72/MasterCard_early_1990s_logo.png',
    'https://c7.hotpng.com/preview/400/28/996/credit-card-computer-icons-visa-electron-bank-curio.jpg',
]


def random_payment_image():
    return random.choice(payment_images)


class PaymentMethod(models.Model):
    title = models.CharField(max_length=32, default="mocked")
    image = models.CharField(max_length=128, default=random_payment_image)
    # TODO: Unmock and use real payment service
    payment_service = models.CharField(max_length=32)
    payment_id = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
