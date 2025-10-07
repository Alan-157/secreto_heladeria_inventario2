# accounts/models.py
from django.db import models

class UserPerfil(models.Model):
    nombre = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)  # <-- nuevo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.nombre

class UsuarioApp(models.Model):  # renombrado si antes usabas "User"
    user_perfil = models.ForeignKey(UserPerfil, on_delete=models.PROTECT, related_name="usuarios")
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)  # <-- opcional (para activar/desactivar usuario)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.email

class UserPerfilAsignacion(models.Model):
    user = models.ForeignKey(UsuarioApp, on_delete=models.CASCADE, related_name="asignaciones")
    perfil = models.ForeignKey(UserPerfil, on_delete=models.CASCADE, related_name="asignaciones")
    activo = models.BooleanField(default=True)  
    assigned_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "perfil")  # <-- evita duplicados exactos
    def __str__(self): return f"{self.user.email} → {self.perfil.nombre}"
