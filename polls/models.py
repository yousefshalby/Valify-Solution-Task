from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-expire_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='choice_user', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="choices_poll", on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='thread_user', on_delete=models.CASCADE)
    Question = models.ForeignKey(Question, related_name="thread_poll", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
