from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models
from django.utils.translation import gettext_lazy as _

from authapp.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(self, phone, is_active=True, is_admin=False, password=None):
        if not phone:
            raise ValueError("Users must have an phone number!")

        user = self.model(
            phone=phone,
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone=phone,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=_("phone number"),
    )

    is_active = models.BooleanField(default=True, verbose_name=_("active"))
    is_admin = models.BooleanField(default=False, verbose_name=_("admin"))

    objects = BaseUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self) -> str:
        return self.phone

    def is_staff(self) -> bool:
        return self.is_admin


class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("user profile"),
    )
    first_name = models.CharField(max_length=50, verbose_name=_("first name"))
    last_name = models.CharField(max_length=50, verbose_name=_("last name"))
    email = models.EmailField(unique=True, max_length=255, verbose_name=_("email"))

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
