from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class RegistrationApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EmailVerificationApiView(APIView):
    pass


class LoginApiView(APIView):
    pass


class RefreshApiView(APIView):
    pass
