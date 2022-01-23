from django.test import TestCase
from voters.serializers import UserSerializer
from django.contrib.auth import get_user_model
from voters.factories import UserFactory


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = UserFactory()
        self.serializer = UserSerializer(instance=self.user)
        self.data = {
            'username': "test",
            "email": "test@test.com",
            "password": "secret",
            "confirm_password": "secret"
        }

    def test_it_contains_all_expected_fields(self):
        """
             result : returning the correct fields for the serializer
        """
        data = self.serializer.data
        self.assertEquals(set(data.keys()), {'username', 'email'})

    def test_email_is_required(self):
        """
              set Up :
                - we are removing the email value and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data.pop('email')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), {'email'})

    def test_it_return_validation_error_when_email_does_not_correct(self):
        """
              set Up :
                - we are updating email value with invalid data and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data['email'] = 'bad email'
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), {'email'})

    def test_username_is_required(self):
        """
              set Up :
                - we are removing the username value and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data.pop('username')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'username'})

    def test_it_returns_validation_error_when_password_does_not_provided(self):
        """
              set Up :
                - we are removing the password value and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data.pop('password')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'password'})

    def test_confirm_password_is_required(self):
        """
              set Up :
                - we are removing the confirm_password value and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data.pop('confirm_password')
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'confirm_password'})

    def test_it_returns_validation_error_when_confirm_password_does_not_match_password(self):
        """
              set Up :
                - we are updating confirm_password value with no match password data and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data['confirm_password'] = 'no matching'
        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'confirm_password'})

    def test_it_returns_validation_errors_when_password_and_confirm_password_does_not_exist_on_create(self):
        """
              set Up :
                - we are removing the password and confirm_password value and check if serializer will be valid
              result : returning serializer not valid
        """
        self.data.pop('password')
        self.data.pop('confirm_password')
        serializer = UserSerializer(data=self.data, context={'is_created': False})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(set(serializer.errors.keys()), {'password', 'confirm_password'})

    def test_it_remove_confirm_password_from_validated_data_when_update(self):
        """
              set Up :
                - we are removing the is created context and check if serializer will be valid
              result : returning serializer not valid
        """
        user = UserFactory()
        serializer = UserSerializer(data=self.data, instance=user, context={'is_created': True})
        serializer.is_valid()
        instance = serializer.save()
        self.assertEquals(serializer.data['username'], instance.username)

    def test_username_field_equals_user_in_user_object(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)

    def test_email_field_equals_email_in_user_object(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_it_remove_confirm_password_from_validated_data_when_create(self):
        serializer = UserSerializer(data=self.data, context={'is_created': True})
        serializer.is_valid()
        instance = serializer.save()
        self.assertIsInstance(instance, self.UserModel)
