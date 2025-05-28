from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.registration_date = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100)
    phone_number = models.CharField(unique=True, max_length=20)
    address = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True, default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'users'

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Товар {self.name}'

    class Meta:
        db_table = 'products'