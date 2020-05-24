from django.contrib import admin

from .models import User, PaymentMethod

admin.site.register(User)
admin.site.register(PaymentMethod)
