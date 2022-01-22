from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, EmailVerificationSerializer, LoginSerializer
from .models import MyToken, MyRefreshToken
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from .utils import create_confirmation_number
from .models import User


class RegistrationApiView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            cache.set('user_data', request.data, 600)  # 10 minutes
            username = serializer.validated_data['username']
            send_mail(
                f'message from the poll app to {username} verify your account please enter the 6-digit number to confirm',
                create_confirmation_number(),
                settings.EMAIL_HOST_USER,
                [serializer.validated_data['email']],
            )
            return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/voter/verifiy/')
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EmailVerificationApiView(APIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if cache.get('otp'):
                if serializer.validated_data['verification_number'] == cache.get('otp'):
                    request.user.is_email_verified = True
                    user_serializer = cache.get('user_data')
                    user_data = UserSerializer(data=user_serializer)
                    user_data.is_valid()
                    user_data.save()
                    user = User.objects.get(email=user_data.validated_data.get('email'))
                    token = MyToken.objects.create(user=user)
                    return Response({"msg": "your account has been created", "Token": token.key},
                                    status=status.HTTP_201_CREATED)
                return Response({"msg": "you have entered the wrong number"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "your otp number is expired please Register again"})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginApiView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = MyToken.objects.get_or_create(user=user)
        return Response({'token': token.key})


class RefreshApiView(APIView):

    def post(self, request, *args, **kwargs):
        token_key = request.auth.key
        token = MyToken.objects.get(key=token_key)
        refresh_token = MyRefreshToken.objects.create(new_user=token.user)
        return Response({"Token": token.key,
                         "Refresh Token access key": refresh_token.access_key,
                         "Refresh Token new Refresh Key": refresh_token.refresh_token_key})
