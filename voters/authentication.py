from rest_framework.authentication import TokenAuthentication
from voters.models import MyToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
import pytz
from django.conf import settings


class MyOwnTokenAuthentication(TokenAuthentication):
    model = MyToken

    def authenticate_credentials(self, key, request=None):

        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=key)
            refresh_token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Invalid or Inactive Token", "is_authenticated": False}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Invalid user", "is_authenticated": False}
            )

        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - settings.ACCESS_TOKEN:
            raise AuthenticationFailed(
                {"error": "Token has expired", "is_authenticated": False}
            )

        if refresh_token.created < utc_now - settings.REFRESH_TOKEN:
            raise AuthenticationFailed(
                {"error": "Refresh token has expired", "is_authenticated": False}
            )

        return token.user, token, refresh_token
