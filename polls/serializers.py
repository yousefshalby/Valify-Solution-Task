from rest_framework import serializers
from .models import Poll, Thread, Choice
from voters.serializers import UserSerializer


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread


class ChoiceSerializer(serializers.ModelSerializer):
    choice_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice

    def get_choice_count(self, obj):
        if obj:
            return obj.count()
        return 0
