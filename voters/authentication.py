from rest_framework.authentication import TokenAuthentication
from voters.models import MyOwnToken


class MyOwnTokenAuthentication(TokenAuthentication):
    model = MyOwnToken
