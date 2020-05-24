from rest_framework import serializers

from .models import User, PaymentMethod


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email',)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password_hash')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password_hash')


class PaymentMethodResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('title', 'image', 'payment_service')


class PaymentMethodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('payment_service', 'payment_id', 'title')
