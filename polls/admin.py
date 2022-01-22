from django.contrib import admin
from .models import Question, Choice, Thread


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'expire_at', 'status']
    list_filter = ['title', 'expire_at']
    list_editable = ['description', 'expire_at', 'status']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'text', 'id', 'votes', 'user_has_voted']
    list_filter = ['text']
    list_editable = ['votes', 'text', 'user_has_voted']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'title', 'content', 'id']


