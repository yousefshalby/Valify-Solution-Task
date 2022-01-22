from django.db import models
from django.conf import settings


class Question(models.Model):
    STATUS = (
        ('Expired', 'Expired'),
        ('NOT Expired', 'NOT Expired'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, blank=True, null=True)
    user_has_voted = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ["-expire_at"]

    def __str__(self):
        return self.title

    @property
    def choices_count(self):
        for choice in self.poll_question.all():
            return choice.votes


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='choice_user', on_delete=models.CASCADE, blank=True,
                             null=True)
    question = models.ForeignKey(Question, related_name="poll_question", on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='thread_user', on_delete=models.CASCADE, blank=True,
                             null=True)
    question = models.ForeignKey(Question, related_name="thread_poll", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)

    def __str__(self):
        return self.title
