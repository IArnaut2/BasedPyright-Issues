from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.
class CustomUserManager(UserManager):
    def create_user(self, email: str, password=None, **other_fields):
        if email is None:
            raise ValueError("Email is required")
        email = self.normalize_email(email=email, **other_fields)
        user: CustomUser = self.model()
        user.set_password(password)
        user.save()
        return user # [1]


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email.split("@")[0]


# [1] https://testdriven.io/blog/django-custom-user-model/
