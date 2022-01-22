from rest_framework import serializers
from .models import Question, Thread, Choice
from voters.models import User


class QuestionSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    choices = serializers.SerializerMethodField()
    threads = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'expire_at', 'choices', 'vote_count', 'status', 'threads']

    def get_choices(self, obj):
        c_qs = Choice.objects.filter(question_id=obj.id)
        choices = ChoiceSerializer(c_qs, many=True).data
        return choices

    def get_threads(self, obj):
        c_qs = Thread.objects.filter(question_id=obj.id)
        threads = ThreadSerializer(c_qs, many=True).data
        return threads

    def get_vote_count(self, obj):
        return obj.choices_count


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    choice_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Choice
        fields = ['user', 'choice_id', 'question']


class ThreadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)

    class Meta:
        model = Thread
        fields = ['user', 'id', 'title', 'description', 'question']
