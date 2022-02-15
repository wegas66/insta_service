from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """Модель кастомного пользователя"""

    email = models.EmailField(
        "email пользователя",
        max_length=260,
        unique=True
    )
    is_active = models.BooleanField("Активный аккаунт", default=False)
    is_admin = models.BooleanField("Статус суперпользователя", default=False)
    staff = models.BooleanField("Статус персонала", default=False)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Список пользателей'
