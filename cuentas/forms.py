from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

User = get_user_model()

# Reglas que se cambian en un solo lugar
EDAD_MIN = 15
EDAD_MAX = 29


def errores_a_dict(form):
    """{'campo': 'primer mensaje'}: el formato que esperan las plantillas."""
    return {campo: lista[0] for campo, lista in form.errors.items()}


class RegistroBaseForm(forms.Form):
    nombre = forms.CharField(
        max_length=30,
        error_messages={
            'required': 'Escribe tu nombre.',
            'max_length': 'Usa hasta 30 caracteres.',
        },
    )
    apellidos = forms.CharField(
        max_length=60,
        error_messages={
            'required': 'Escribe tus apellidos.',
            'max_length': 'Usa hasta 60 caracteres.',
        },
    )
    username = forms.CharField(
        max_length=30,
        validators=[RegexValidator(
            r'^[\w.-]+$',
            'Usa solo letras, números, puntos, guiones y guion bajo.',
        )],
        error_messages={
            'required': 'Elige un nombre de usuario.',
            'max_length': 'Usa hasta 30 caracteres.',
        },
    )
    correo = forms.EmailField(
        max_length=254,
        error_messages={
            'required': 'Escribe tu correo electrónico.',
            'invalid': 'Escribe un correo válido, por ejemplo nombre@ejemplo.com.',
        },
    )
    contrasena = forms.CharField(
        strip=False,
        error_messages={'required': 'Crea una contraseña.'},
    )
    contrasena2 = forms.CharField(
        strip=False,
        error_messages={'required': 'Confirma tu contraseña.'},
    )
    terminos = forms.BooleanField(
        error_messages={
            'required': 'Acepta los términos y el aviso de privacidad para continuar.',
        },
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Ese nombre de usuario ya está en uso. Prueba con otro.')
        return username

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if User.objects.filter(email__iexact=correo).exists():
            raise ValidationError('Ya existe una cuenta con ese correo. Inicia sesión o usa otro.')
        return correo

    def clean_contrasena(self):
        contrasena = self.cleaned_data['contrasena']
        try:
            validate_password(contrasena)
        except ValidationError as error:
            raise ValidationError(error.messages[0])
        return contrasena

    def clean(self):
        datos = super().clean()
        contrasena = datos.get('contrasena')
        contrasena2 = datos.get('contrasena2')
        if contrasena and contrasena2 and contrasena != contrasena2:
            self.add_error('contrasena2', 'Las contraseñas no coinciden. Escríbelas de nuevo.')
        return datos


class RegistroUsuarioForm(RegistroBaseForm):
    fecha_nacimiento = forms.DateField(
        error_messages={
            'required': 'Indica tu fecha de nacimiento.',
            'invalid': 'Escribe una fecha válida.',
        },
    )
    ciudad = forms.CharField(
        max_length=50,
        error_messages={
            'required': 'Escribe tu ciudad.',
            'max_length': 'Usa hasta 50 caracteres.',
        },
    )

    def clean_fecha_nacimiento(self):
        nacimiento = self.cleaned_data['fecha_nacimiento']
        hoy = date.today()
        edad = hoy.year - nacimiento.year - (
            (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)
        )
        if edad < EDAD_MIN or edad > EDAD_MAX:
            raise ValidationError(f'Rishine es para jóvenes de {EDAD_MIN} a {EDAD_MAX} años.')
        return nacimiento


class RegistroPromotorForm(forms.Form):
    organizacion = forms.CharField(
        max_length=50,
        error_messages={
            'required': 'Escribe el nombre de tu organización.',
            'max_length': 'Usa hasta 50 caracteres.',
        },
    )
    telefono = forms.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\+?[\d\s-]{8,15}$',
            'Escribe un teléfono válido, por ejemplo 3312345678.',
        )],
        error_messages={
            'required': 'Escribe tu número de teléfono.',
            'max_length': 'Usa hasta 15 caracteres.',
        },
    )