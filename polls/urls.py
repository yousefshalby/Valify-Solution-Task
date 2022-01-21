from django.urls import path
from .views import GetPolls, VotePolls

app_name = "polls"

urlpatterns = [
    path('', GetPolls, name='list'),
    path('create/<int:question_id>/', VotePolls, name='post-vote'),
]
