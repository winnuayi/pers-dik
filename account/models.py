from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=self.normalize_email(email),
                          is_staff=is_staff,
                          is_active=False,
                          is_superuser=is_superuser,
                          # last_login=timezone.now(),
                          # date_joined=timezone.now(),
                          **extra_fields)

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # ATTRIBUTE WAJIB
    email = models.CharField(u'Email', max_length=50, unique=True)
    fullname = models.CharField(max_length=100)

    # true untuk top management dan staf HR
    # false untuk karyawan lainnya
    is_staff = models.BooleanField(default=False,
                                   help_text="Hanya untuk CEO, CTO, dan PMO")
    # untuk mengaktivasi dan deaktivasi akun
    is_active = models.BooleanField(default=False,
                                    help_text="Centang agar bisa masuk aplikasi")

    # konfigurasi: login menggunakan spesifik attribute (disarankan email)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Akun'

    def get_short_name(self):
        return self.fullname
