from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid
from datetime import datetime, timedelta, date
from django.utils.timezone import now
from asgiref.sync import async_to_sync
from django.urls import reverse

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_kwargs)
        user.set_password(password)
        user.is_active = extra_kwargs.get('is_active', True) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_kwargs):
        user = self.create_user(
            email,
            password=password,
            **extra_kwargs
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='useraccount_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='useraccount_permissions_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username



