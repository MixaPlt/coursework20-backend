from django.urls import path

from .views import UserView, RegistrationView, MeView, LoginView, PaymentsView

urlpatterns = [
    path('user/all', UserView.as_view()),
    path('user/registration', RegistrationView.as_view()),
    path('user/me', MeView.as_view()),
    path('user/login', LoginView.as_view()),
    path('payments/', PaymentsView.as_view()),
]
 