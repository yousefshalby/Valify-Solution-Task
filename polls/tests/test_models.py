from django.test import TestCase
from polls.models import Question, Choice, Thread


class TestQuestion(TestCase):
    """
        set Up : we are creating an object from question model
        result : stringify new object title
    """

    def test_it_stringify_question_title(self):
        question = Question.objects.create(title='book')
        old_question = Question.objects.get(pk=1)
        self.assertEqual(str(old_question), question.title)


class TestChoice(TestCase):
    """
        set Up : we are creating an object from choice model
        result : stringify new object text
    """

    def test_it_stringify_choice_text(self):
        question = Question.objects.create(title='book')
        choice = Choice.objects.create(text='choice', question_id = question.id)
        old_choice = Choice.objects.get(pk=1)
        self.assertEqual(str(old_choice), choice.text)


class TestThread(TestCase):
    """
        set Up : we are creating an object from thread model
        result : stringify new object title
    """

    def test_it_stringify_thread_title(self):
        thread = Thread.objects.create(title='cats')
        old_thread = Thread.objects.get(pk=1)
        self.assertEqual(str(old_thread), thread.title)
