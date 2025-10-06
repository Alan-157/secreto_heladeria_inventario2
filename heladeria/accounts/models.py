from django.db import models

class UserPerfil(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    user_perfil = models.ForeignKey(UserPerfil, on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


