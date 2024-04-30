# This module provides an authentication backend wwhich enables users to log in using their email address
# Based on the forum answer at https://stackoverflow.com/a/37332393

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
