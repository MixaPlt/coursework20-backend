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

    def post(self, request):
        user = request.data.get('user')
        serializer = RegistrationSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.validated_data.get('email'))[:1]
            if user:
                return HttpResponseServerError({"{\"error\": \"Such user already exists\"}"})
            user_saved = serializer.save()
        response = Response({"success": "User successfully created"})
        response['session-token'] = user_saved.token
        return response
