from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import UserApproval

User = get_user_model()


class LoginForm(forms.Form):
    login = forms.CharField(
        label="Usuario ou e-mail",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "username",
                "placeholder": "Seu usuario ou e-mail",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "current-password",
                "placeholder": "Sua senha",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Usuario/e-mail ou senha invalidos.",
        "pending": "Seu cadastro ainda esta aguardando aprovacao de um administrador.",
        "rejected": "Seu cadastro nao foi aprovado. Procure um administrador do ChaveRadar.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        login_value = (cleaned_data.get("login") or "").strip()
        password = cleaned_data.get("password")

        if not login_value or not password:
            return cleaned_data

        user = User.objects.filter(username__iexact=login_value).first()
        if user is None:
            user = User.objects.filter(email__iexact=login_value).first()

        if user is None or not user.check_password(password):
            raise forms.ValidationError(self.error_messages["invalid_login"], code="invalid_login")

        if not user.is_active:
            approval = getattr(user, "approval_request", None)
            if approval and approval.status == UserApproval.STATUS_REJECTED:
                raise forms.ValidationError(self.error_messages["rejected"], code="rejected")
            raise forms.ValidationError(self.error_messages["pending"], code="pending")

        self.user_cache = authenticate(
            self.request,
            username=user.get_username(),
            password=password,
        )
        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages["invalid_login"], code="invalid_login")

        return cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)
    email = forms.EmailField(label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "Seu nome",
            "last_name": "Seu sobrenome",
            "email": "voce@empresa.com.br",
            "username": "Escolha um usuario",
            "password1": "Crie uma senha",
            "password2": "Repita a senha",
        }
        autocomplete = {
            "first_name": "given-name",
            "last_name": "family-name",
            "email": "email",
            "username": "username",
            "password1": "new-password",
            "password2": "new-password",
        }
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": placeholders.get(name, ""),
                    "autocomplete": autocomplete.get(name, "off"),
                }
            )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe um cadastro com este e-mail.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.is_active = False

        if commit:
            user.save()
            UserApproval.objects.get_or_create(
                user=user,
                defaults={"status": UserApproval.STATUS_PENDING},
            )
        return user
