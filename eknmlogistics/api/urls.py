from django.urls import path

from .views import UserView, RegistrationView

urlpatterns = [
    path('user/all', UserView.as_view()),
    path('user/registration', RegistrationView.as_view()),
]
