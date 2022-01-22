from django.urls import path
from .views import RefreshApiView, RegistrationApiView, LoginApiView, EmailVerificationApiView

app_name = "voters"

urlpatterns = [

    path('register/', RegistrationApiView.as_view(), name='register'),
    path('verifiy/', EmailVerificationApiView.as_view(), name='email-verification'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('refresh/', RefreshApiView.as_view(), name='refresh'),

]
