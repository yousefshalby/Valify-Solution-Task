from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

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
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', "id"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = get_user_model().objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):
    verification_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['verification_number']


