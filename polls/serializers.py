from rest_framework import serializers
from .models import Question, Thread, Choice
from voters.models import User


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    Question = QuestionSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = ['user', 'id', 'title', 'description', 'Question']


class ChoiceSerializer(serializers.ModelSerializer):
    Question = QuestionSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Choice
        fields = ['user', 'id', 'is_active', 'question', 'votes']


class VoteSerializer(serializers.Serializer):  # noqa
    choice_id = serializers.IntegerField()
