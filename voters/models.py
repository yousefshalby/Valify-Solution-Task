from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
import binascii
import os
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken


class MyToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True, db_index=True, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(MyToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    @property
    def create_confirmation_number(self):
        return get_random_string(length=6, allowed_chars='1234567890')


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def send_mail_on_create(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'message from the poll app to {instance.username} to verify you account so please enter the 6-digit number to confirm',
            instance.create_confirmation_number,
            instance.email,
            settings.EMAIL_HOST_USER,
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        MyToken.objects.create(user=instance)
