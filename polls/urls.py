from django.urls import path
from .views import GetPolls, VotePolls

app_name = "polls"

urlpatterns = [
    path('', GetPolls.as_view(), name='list'),
    path('create/<int:question_id>/', VotePolls.as_view(), name='post-vote'),
]
