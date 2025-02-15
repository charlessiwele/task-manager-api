from django.db import models
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        if not username:
            raise ValueError('Username is Required')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(username, email, password, **extra_fields)


class Status(models.Model):
    name = models.CharField(
        max_length=50, 
        blank=False, 
        null=False,
        unique=True,
        help_text=(
            "Required. Status name, 50 characters or fewer."
        ),
        error_messages={
            "unique": ("A Status with this name already exists."),
        }
    )
    description = models.CharField(max_length=500, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=1500, blank=False, null=False)
    due_date = models.DateTimeField(default=timezone.now, blank=False, null=False)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
