from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from authentication.models import *

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager para perfiles de usuario"""

    def create_user(self, email, name, password=None):
        """Crear nuevo perfil de usuario"""
        if not email:
            raise ValueError('El usuario debe tener un email')

        email = self.normalize_email(email)
        user = self.model(email = email, name= name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin,models.Model):
    """Modelo base de Datos para usuarios """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        '''Obtener nombre completo'''
        return self.name

    def get_short_name(self):
        '''Obtener nombre corto'''
        return self.name

    def __str__(self):
        return self.email

class Cuadro(models.Model):
    """Modelo con los datos de cada cuadro a tokenizar"""   
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='static/paintings/%Y/%m/%d')
    
    #user = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='paint', unique=False, blank=True, null=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='paint', unique=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    

    class Meta:
        db_table = 'Cuadro'
        ordering = ['name']
        verbose_name = "cuadro"
        verbose_name_plural = "Cuadros"
        
        
        
