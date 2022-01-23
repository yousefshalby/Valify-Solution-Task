from django.test import TestCase
from django.urls import reverse, resolve
from voters.views import RefreshApiView, RegistrationApiView, LoginApiView, EmailVerificationApiView


class VoterUrlsTestCase(TestCase):
    def test_refresh_url_resolves(self):
        """
                  set Up : we are calling the refresh token url
                result : returning the correct view for the url
        """
        url = reverse('voters:refresh')
        self.assertEquals(resolve(url).func.view_class, RefreshApiView)

    def test_email_verification_url_resolves(self):
        """
                set Up : we are calling email verification url
                result : returning the correct view for the url
        """
        url = reverse('voters:email-verification')
        self.assertEquals(resolve(url).func.view_class, EmailVerificationApiView)

    def test_user_login_url_resolves(self):
        """
                set Up : we are calling login url
                result : returning the correct view for the url
        """
        url = reverse('voters:login')
        self.assertEquals(resolve(url).func.view_class, LoginApiView)

    def test_user_registration_url_resolves(self):
        """
                set Up : we are calling the registration url
                result : returning the correct view for the url
        """
        url = reverse('voters:register')
        self.assertEquals(resolve(url).func.view_class, RegistrationApiView)
