from django.http import HttpResponseServerError
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .maps import reverse_geocode, route_waypoints
from .serializers import *


def get_user_from_request(request):
    token = request.META.get('HTTP_SESSION_TOKEN', None)
    token_user = User.objects.filter(token=token)[:1][0]
    return token_user


@permission_classes((permissions.AllowAny,))
class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})


@permission_classes((permissions.AllowAny,))
class RegistrationView(APIView):
    def post(self, request):
        global user_saved
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.validated_data.get('email'))[:1]
            if user:
                return HttpResponseServerError({"{\"error\": \"Such user already exists\"}"})
            user_saved = serializer.save()
        response_serializer = UserSerializer(user_saved)
        response = Response({"user": response_serializer.data})
        response['session-token'] = user_saved.token
        return response


@permission_classes((permissions.AllowAny,))
class MeView(APIView):
    def get(self, request):
        user = get_user_from_request(request)
        if not user:
            return HttpResponseServerError({"error: Invalid token"})
        serializer = UserSerializer(user)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class LoginView(APIView):
    def post(self, request):
        global user
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.validated_data.get('email'))[:1][0]
            if not user:
                return HttpResponseServerError({"error: email not found"})
            elif user.password_hash != serializer.validated_data.get('password_hash'):
                return HttpResponseServerError({"error: incorrect password"})

        response_serializer = UserSerializer(user)
        response = Response({"user": response_serializer.data})
        response['session-token'] = user.token
        return response


@permission_classes((permissions.AllowAny,))
class PaymentsView(APIView):
    def post(self, request):
        user = get_user_from_request(request)
        payment_serializer = PaymentMethodRequestSerializer(data=request.data)
        if user and payment_serializer.is_valid(raise_exception=True):
            payment_method = payment_serializer.save(owner=user)
            return Response({"Successfully added"})
        return HttpResponseServerError()

    def get(self, request):
        user = get_user_from_request(request)
        if (not user):
            return HttpResponseServerError("Not authorized")
        user_methods = PaymentMethod.objects.filter(owner=user)
        serializer = PaymentMethodResponseSerializer(user_methods, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ReverseGeocodeView(APIView):
    def get(self, request):
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        if not latitude or not longitude:
            return HttpResponseServerError('No params')
        google_response = reverse_geocode(latitude, longitude)['results'][0]['address_components']

        def item_by_type(type):
            x = None
            return [x for x in google_response if type in x['types']]

        try:
            street = item_by_type('route')[0]['short_name']
            street_number = item_by_type('street_number')
            formatted = street
            if street_number:
                formatted += ", " + street_number[0]['short_name']
            return Response(formatted)
        except:
            return Response("Unnamed road")


@permission_classes((permissions.AllowAny,))
class CreateRouteView(APIView):
    def post(self, request):
        origin_lat = request.query_params.get('origin_lat')
        origin_lng = request.query_params.get('origin_lng')
        destination_lat = request.query_params.get('destination_lat')
        destination_lng = request.query_params.get('destination_lng')

        raw_points = route_waypoints(origin_lat, origin_lng, destination_lat, destination_lng)
        points = {'points': raw_points}
        return Response(points)


@permission_classes((permissions.AllowAny,))
class NearDrivers(APIView):
    def get(self, request):
        from .drivers import driver
        response = []
        drivers = driver.provide_drivers()
        for cord in drivers:
            latlng = cord.location()
            response.append({
                "latitude": latlng[0],
                "longitude": latlng[1],
                "accuracy": 0,
            })
        return Response(response)