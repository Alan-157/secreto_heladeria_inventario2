from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        widgets = {
            "password": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso.")
        return email
    
    def password_min(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if len(password) > 20:
            raise forms.ValidationError("La contraseña no debe exceder los 20 caracteres.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        self.password_min()
        return password
    
    def password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):    
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False)  # Campo para "Recordarme"
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Credenciales inválidas.")
            except User.DoesNotExist:
                raise forms.ValidationError("Credenciales inválidas.")
        return cleaned_data