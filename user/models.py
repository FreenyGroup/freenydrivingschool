from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager): # 1.

    def create_user(self, email, first_name, last_name, password=None): # 2.
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
            
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, first_name, last_name, password=None): # 3.
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser,PermissionsMixin):
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address', unique=True)
    dob = models.DateField('date of birth',null=True,blank=True,)
    nickname = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,11}$', message='Phone number must be 9-11 characters', code='invalid_phone_number')], max_length=11, null=True,blank=True) 
    ship_address = models.CharField('address',max_length=250, null=True,blank=True)
    address2 = models.CharField('apt',max_length=250, null=True,blank=True)
    locality = models.CharField('city',max_length=250, null=True,blank=True)
    state = models.CharField('state',max_length=250, null=True,blank=True)
    postcode = models.CharField('zipcode',max_length=250, null=True,blank=True)
    country = models.CharField('country',max_length=250, null=True,blank=True)
    bio = models.TextField('bio',max_length=500,null=True,blank=True)
    username = None # 2.

    objects = CustomUserManager() # 4.

    USERNAME_FIELD = 'email' # 5.
    REQUIRED_FIELDS = ['first_name','last_name'] # 6.
