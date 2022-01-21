from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MyToken
from .serializers import EmailVerificationSerializer


class RegistrationApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EmailVerificationApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = EmailVerificationSerializer(instance=request.data)
        if serializer.is_valid():
            if serializer.validated_data['verification_number'] == request.user.create_confirmation_number:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"msg": "you have entered the wrong number"})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginApiView(APIView):
    def get(self, request, *args, **kwargs):
        token_key = request.headers.get('Authorization').split(' ')[1]
        token = MyToken.objects.get(key=token_key)
        serializer = UserSerializer(instance=token.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshApiView(APIView):
    pass
