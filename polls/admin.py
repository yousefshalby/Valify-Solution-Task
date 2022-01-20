from django.contrib import admin
from .models import Question, Choice, Thread

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'expire_at']
    list_filter = ['title', 'expire_at']
    list_editable = ['title', 'description', 'expire_at']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'Question', 'text', 'is_active', 'id']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['user', 'Question', 'title', 'content', 'id']


