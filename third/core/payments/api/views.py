from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer, PaymentSerializer, ChangePasswordSerializer, EmailOrUsernameAuthTokenSerializer, PaymentResponseSerializer, payment_schema
from django.contrib.auth import update_session_auth_hash


@swagger_auto_schema(
    methods=['POST'],
    request_body=UserSerializer(), 
    responses={  
        status.HTTP_201_CREATED: UserSerializer(),
        status.HTTP_400_BAD_REQUEST: "Error",
    },
)
@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=['POST'],
    request_body=EmailOrUsernameAuthTokenSerializer(),
    responses={ 
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            description='Token',
        ), 
        status.HTTP_401_UNAUTHORIZED: "Error", 
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = EmailOrUsernameAuthTokenSerializer(data=request.data)

    if serializer.is_valid():
        username_or_email = serializer.validated_data.get('username_or_email')
        password = serializer.validated_data.get('password')

        user = None

        user = authenticate(request=request, username=username_or_email, password=password)

        if not user:
            user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
            if user:
                user = authenticate(request=request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=payment_schema,
    ),
    responses={  
        status.HTTP_200_OK: PaymentResponseSerializer(), 
        status.HTTP_400_BAD_REQUEST: "Error",  
    },
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payments_view(request):
    payments = request.data
    serializer = PaymentSerializer(data=payments, many=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    TAX = 0.16
    COMISSION_PERCENTAGE = 0.03
    TAX_EXEMPTION = 500
    USD_TO_MXN = 20

    total_before_taxes = 0
    total_taxes = 0
    commissions = 0


    for payment in payments:
        currency = payment['currency']
        amount = payment['amount'] if currency == 'MXN' else payment['amount'] * USD_TO_MXN
        
        total_before_taxes += amount
        
        if  amount > TAX_EXEMPTION:
            total_taxes += amount * TAX

        if currency == 'USD':
            commissions += amount * COMISSION_PERCENTAGE

    response_data = {
        'total_before_taxes': total_before_taxes,
        'total_taxes': total_taxes,
        'commissions': commissions,
    }

    response_serializer = PaymentResponseSerializer(response_data)
    return Response(response_serializer.data)

@swagger_auto_schema(
    methods=['POST'],
    request_body=ChangePasswordSerializer(),
    responses={ 
        status.HTTP_200_OK: "Success", 
        status.HTTP_400_BAD_REQUEST: "Error", 
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    current_password = serializer.validated_data['current_password']
    new_password = serializer.validated_data['new_password']
    confirm_password = serializer.validated_data['confirm_password']

    if not user.check_password(current_password):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    update_session_auth_hash(request, user)

    return Response("Password changed successfully", status=status.HTTP_200_OK)