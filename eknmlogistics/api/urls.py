from django.urls import path

from .views import *

urlpatterns = [
    path('user/all', UserView.as_view()),
    path('user/registration', RegistrationView.as_view()),
    path('user/me', MeView.as_view()),
    path('user/login', LoginView.as_view()),
    path('payments/', PaymentsView.as_view()),
    path('maps/reverse_geocode', ReverseGeocodeView.as_view()),
    path('maps/create_route', CreateRouteView.as_view()),
    path('maps/near_drivers', NearDrivers.as_view()),
]
 