"""
https://github.com/django/django/blob/master/django/contrib/auth/models.py
"""

from django.contrib import auth
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied

from sisfoops.models import OpsCustomuser as CustomUser


class ExternalModelBackend(BaseBackend):
    """
    Ganti EXTERNAL_DATABASE untuk login menggunakan external database.

    Tambahkan line berikut di settings.py
    AUTHENTICATION_BACKENDS = ['account.backends.ExternalModelBackend']
    """

    # nama external database
    EXTERNAL_DATABASE = 'sisfoops'

    def authenticate(self, request, username=None, password=None):
        """Autentikasi menggunakan legacy database AnevData."""
        # validate parameters.
        if username is None or password is None:
            return

        try:
            user = CustomUser.objects.using(self.EXTERNAL_DATABASE) \
                                     .get(email=username)
        # TODO UserModel.DoesNotExist dan database sisfoops down
        except Exception:
            return

        if check_password(password, user.password) and user.is_active == True:
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.using(self.EXTERNAL_DATABASE) \
                                     .get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
