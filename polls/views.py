from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import pytz

from .serializers import QuestionSerializer, ChoiceSerializer
from django.shortcuts import get_object_or_404
from .models import Question, Choice
from django.utils import timezone
from rest_framework import filters
from voters.authentication import MyOwnTokenAuthentication, MyRefreshTokenAuthentication
from .pagination import PostPageNumberPagination
from rest_framework.generics import ListAPIView


class GetPolls(ListAPIView):
    authentication_classes = [MyOwnTokenAuthentication, MyRefreshTokenAuthentication]
    queryset = Question.objects.all().order_by('-expire_at')
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'description', 'poll_question__text']
    pagination_class = PostPageNumberPagination


class VotePolls(APIView):
    authentication_classes = (MyOwnTokenAuthentication, MyRefreshTokenAuthentication)
    serializer_class = ChoiceSerializer

    def post(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        if utc_now < question.expire_at:
            if not question.poll_question.filter(user_has_voted=True).exists():
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    choice = get_object_or_404(Choice, pk=serializer.validated_data.get('id'), question=question)
                    choice.votes += 1
                    choice.user_has_voted = True
                    choice.save()
                    return Response({"msg": "Voted successfully "}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response({"msg": "you already voted for this poll"})
        return Response({"msg": "this Poll is Expired"}, status=status.HTTP_400_BAD_REQUEST)
