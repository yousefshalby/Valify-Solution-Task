from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import QuestionSerializer, ChoiceSerializer, ThreadSerializer, VoteSerializer
from django.shortcuts import get_object_or_404
from .models import Question, Choice
from django.utils import timezone


class GetPolls(APIView, LimitOffsetPagination):
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        pass


class VotePolls(APIView):
    serializer_class = ChoiceSerializer

    def post(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        if timezone.now() > question.expire_at:
            if request.user.choice_set.filter(question_id=question_id, votes__gte=0).exists():
                serializer = ChoiceSerializer(data=request.data)
                if serializer.is_valid():
                    choice = get_object_or_404(Choice, pk=serializer.validated_data['id'], question=question)
                    choice.votes += 1
                    choice.save()
                    return Response("Voted successfully ", status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response({"msg": "you already voted for this poll"})
        return Response({"msg": "this Poll is Expired"}, status=status.HTTP_400_BAD_REQUEST)
