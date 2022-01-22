from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('poll/', include('polls.urls', namespace='poll')),
    path('voter/', include('voters.urls', namespace='voters')),
]
