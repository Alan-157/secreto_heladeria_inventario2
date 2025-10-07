from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from accounts.models import UserPerfil, UsuarioApp, UserPerfilAsignacion

# --- ACCIONES PERSONALIZADAS ---
@admin.action(description="Activar perfiles seleccionados")
def activar_perfiles(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} perfil(es) activado(s).", messages.SUCCESS)

@admin.action(description="Desactivar perfiles seleccionados")
def desactivar_perfiles(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} perfil(es) desactivado(s).", messages.WARNING)

@admin.action(description="Activar usuarios seleccionados")
def activar_usuarios(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} usuario(s) activado(s).", messages.SUCCESS)

@admin.action(description="Desactivar usuarios seleccionados")
def desactivar_usuarios(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} usuario(s) desactivado(s).", messages.WARNING)


# --- VALIDACIÓN INLINE ---
class AsignacionInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        vistos_user = set()
        activos_por_user = {}

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE", False):
                continue

            user = form.cleaned_data.get("user")
            activo = form.cleaned_data.get("activo", True)

            if user is None:
                raise ValidationError("Debes seleccionar un usuario.")

            if user in vistos_user:
                raise ValidationError(f"El usuario '{user}' ya está asignado a este perfil.")
            vistos_user.add(user)

            if hasattr(user, "is_active") and not user.is_active:
                raise ValidationError(f"El usuario '{user}' está inactivo; no puede asignarse al perfil.")

            if getattr(self.instance, "is_active", True) is False and activo:
                raise ValidationError("No puedes crear asignaciones activas en un perfil inactivo.")

            if activo:
                activos_por_user[user] = activos_por_user.get(user, 0) + 1

        conflictivos = [u for u, c in activos_por_user.items() if c > 1]
        if conflictivos:
            raise ValidationError("Cada usuario puede tener solo una asignación ACTIVA en este perfil.")


# --- INLINE ---
class UserPerfilAsignacionInline(admin.TabularInline):
    model = UserPerfilAsignacion
    formset = AsignacionInlineFormset
    extra = 0
    fields = ("user", "activo", "assigned_at", "created_at", "updated_at")
    readonly_fields = ("assigned_at", "created_at", "updated_at")
    show_change_link = True


# --- ADMIN: Perfiles ---
@admin.register(UserPerfil)
class UserPerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("nombre",)
    ordering = ("nombre",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [UserPerfilAsignacionInline]
    actions = [activar_perfiles, desactivar_perfiles]


# --- ADMIN: Usuarios ---
@admin.register(UsuarioApp)
class UsuarioAppAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "user_perfil", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at", "user_perfil")
    search_fields = ("email", "name", "user_perfil__nombre")
    ordering = ("email",)
    readonly_fields = ("created_at", "updated_at")
    actions = [activar_usuarios, desactivar_usuarios]


# --- ADMIN: Asignaciones ---
@admin.register(UserPerfilAsignacion)
class UserPerfilAsignacionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "perfil", "activo", "assigned_at", "created_at", "updated_at")
    list_filter = ("activo", "assigned_at", "created_at", "updated_at", "perfil")
    search_fields = ("user__email", "perfil__nombre")
    ordering = ("user",)
    readonly_fields = ("assigned_at", "created_at", "updated_at")
    