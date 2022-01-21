from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import QuestionSerializer, ChoiceSerializer, ThreadSerializer
from django.shortcuts import get_object_or_404
from .models import Question, Choice
from django.utils import timezone
from django.db.models import Prefetch
from rest_framework import filters


class GetPolls(APIView, LimitOffsetPagination):
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'description', 'poll_question']

    def get(self, request, *args, **kwargs):
        all_polls = Question.objects.all().order_by('-expire_at')
        results = self.paginate_queryset(all_polls, request, view=self)
        serializer = QuestionSerializer(instance=results, many=True)
        return self.get_paginated_response(serializer.data)


class VotePolls(APIView):
    serializer_class = ChoiceSerializer

    def post(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        if timezone.now() > question.expire_at:
            if not request.auth.choice_set.prefetch_related(
                    Prefetch('question', queryset=Question.objects.filter(has_voted=True)))\
                    .filter(question_id=question_id).exists():
                serializer = ChoiceSerializer(data=request.data)
                if serializer.is_valid():
                    choice = get_object_or_404(Choice, pk=serializer.validated_data['id'], question=question)
                    choice.votes += 1
                    question.has_voted = True
                    choice.save()
                    return Response({"msg": "Voted successfully "}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response({"msg": "you already voted for this poll"})
        return Response({"msg": "this Poll is Expired"}, status=status.HTTP_400_BAD_REQUEST)
