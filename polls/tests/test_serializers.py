from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.models import Question, Thread, Choice
from polls.serializers import QuestionSerializer, ChoiceSerializer, ThreadSerializer
from voters.factories import UserFactory


class QuestionSerializerTestCase(TestCase):
    def setUp(self):
        self.question = Question.objects.create(title='test', description='test description')
        self.serializer = QuestionSerializer(instance=self.question)
        self.data = {
            "title": 'test',
            "description": 'test description',
            "expire_at": "2019-05-08T09:23:09.424129Z",
            "status": "Expired",
        }

    def test_if_returns_expected_field(self):
        """
              result : returning the correct fields for the serializer
        """
        data = self.serializer.data
        self.assertEquals(set(data.keys()), {'id', 'title', 'description', 'expire_at', 'choices', 'vote_count',
                                             'status', 'threads'})

    def test_question_not_accept_payload_without_title(self):
        """
              set Up :
                - we are removing the title value and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data.pop('title')
        serializer = QuestionSerializer(instance=self.question, data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_question_accept_payload_without_description(self):
        """
              set Up :
                - we are removing the description value and check if serializer will be valid
              result : returning serializer is valid
        """
        self.data.pop('description')
        serializer = QuestionSerializer(instance=self.question, data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_it_returns_error_when_no_data(self):
        """
              set Up :
                  - we are removing all serializer data
              result : returning serializer not valid and number of errors
        """
        serializer = QuestionSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)

    def test_it_creates_question(self):
        """
              set Up :
                - we are giving the right date to the serializer
              result : serializer obj is created successfully
        """
        serializer = QuestionSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_it_updates_question(self):
        """
              set Up :
                - we are creating obj from serializer
                - we are giving the right date to the serializer
              result : serializer obj data will be updated successfully
        """
        serializer = QuestionSerializer(instance=self.question, data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEquals(QuestionSerializer(instance=self.question).data, serializer.data)
