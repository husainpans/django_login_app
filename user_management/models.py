from __future__ import unicode_literals
from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import CharField, EmailField, \
                            ForeignKey, DateTimeField, BooleanField

from user_management import strings

DESIGNATIONS = (
    (strings.ADMIN, strings.ADMIN),
    (strings.STAFF, strings.STAFF),
 )

# Create your models here.

class Users(AbstractBaseUser):
    username = CharField(max_length=20, blank=False, unique = True)
    email = EmailField(max_length=50, blank=False, unique = True)
    firstname = CharField(max_length=20, default='N/A')
    lastname = CharField(max_length=20, default='N/A')
    designation = CharField(choices=DESIGNATIONS,max_length=10, default = "STAFF", blank=False)
    objects = BaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']


    class Meta:
        db_table = 'user'   