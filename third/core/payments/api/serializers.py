from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import  Payment
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password']
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user = self.Meta.model(**validated_data, password=hashed_password)
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user  # Obtener el usuario actual desde la solicitud

        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError("La contraseña actual es incorrecta")

        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Las contraseñas nuevas no coinciden")

        # Hashear la nueva contraseña antes de guardarla
        data['new_password'] = make_password(new_password)

        return data


class PaymentResponseSerializer(serializers.Serializer):
    total_before_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_taxes = serializers.DecimalField(max_digits=10, decimal_places=2)
    commissions = serializers.DecimalField(max_digits=10, decimal_places=2)


class EmailOrUsernameAuthTokenSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()


payment_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
        'currency': openapi.Schema(type=openapi.TYPE_STRING),
    }
)