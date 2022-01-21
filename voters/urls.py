from django.urls import path
from .views import RefreshApiView, RegistrationApiView, LoginApiView, EmailVerificationApiView

app_name = "voters"

urlpatterns = [

    path('register/', RegistrationApiView, name='register'),
    path('create/<int:question_id>/', EmailVerificationApiView, name='email-verification'),
    path('login/', LoginApiView, name='login'),
    path('refresh/', RefreshApiView, name='refresh'),

]
