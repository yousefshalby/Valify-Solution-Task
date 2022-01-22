from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

from voters.models import MyToken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, trim_whitespace=False,
                                     required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, trim_whitespace=False,
                                             required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if self.context:
            if 'password' not in attrs and 'confirm_password' in attrs:
                raise ValidationError({"password": _("password field is required")})
            if 'confirm_password' not in attrs and 'password' in attrs:
                raise ValidationError({"confirm_password": _("confirm password is required")})
            if 'password' in attrs and 'confirm_password' in attrs and attrs['password'] != attrs['confirm_password']:
                raise ValidationError({"confirm_password": _('confirm password does not match password')})

        else:
            if 'password' not in attrs and 'confirm_password' not in attrs:
                raise ValidationError(
                    {"password": _("password field is required"),
                     "confirm_password": _("confirm password is required")})
            if 'password' not in attrs:
                raise ValidationError({"password": _("password field is required")})
            if 'confirm_password' not in attrs:
                raise ValidationError({"confirm_password": _("confirm password is required")})
            if attrs['password'] != attrs['confirm_password']:
                raise ValidationError({"confirm_password": _('confirm password does not match password')})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        try:
            validated_data.pop('confirm_password')
        except:
            pass
        return super(UserSerializer, self).update(instance, validated_data)

    def save(self, **kwargs):
        user = super(UserSerializer, self).save()
        if 'password' in self.validated_data:
            user.set_password(self.validated_data["password"])
            user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'},
                                     trim_whitespace=False, write_only=True)
    token = serializers.CharField(label=_("Token"), read_only=True)
    extra_kwargs = {"password": {"write_only": True}}

    class Meta:
        fields = ['username', 'password', 'token']
        model = MyToken

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmailVerificationSerializer(serializers.ModelSerializer):
    verification_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['verification_number']
