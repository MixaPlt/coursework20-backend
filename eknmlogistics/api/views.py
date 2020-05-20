from django.http import HttpResponseServerError
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, RegistrationSerializer


@permission_classes((permissions.AllowAny,))
class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})


@permission_classes((permissions.AllowAny,))
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.validated_data.get('email'))[:1]
            if user:
                return HttpResponseServerError({"{\"error\": \"Such user already exists\"}"})
            user_saved = serializer.save()
        response = Response({"success": "User successfully created"})
        response['session-token'] = user_saved.token
        return response


@permission_classes((permissions.AllowAny,))
class MeView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_SESSION_TOKEN', None)
        user = User.objects.filter(token=token)[:1][0]
        if not token or not user:
            return HttpResponseServerError({"error: Invalid token"})
        serializer = UserSerializer(user)
        return Response({"user": serializer.data})
