from django.urls import path

from .views import UserView, RegistrationView, MeView

urlpatterns = [
    path('user/all', UserView.as_view()),
    path('user/registration', RegistrationView.as_view()),
    path('user/me', MeView.as_view()),
]
