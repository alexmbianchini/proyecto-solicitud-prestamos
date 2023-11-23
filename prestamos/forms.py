from django.forms import ModelForm
from .models import Solicitante
from django.core.exceptions import ValidationError

class FormularioSolicitante(ModelForm):
    class Meta:
        model = Solicitante
        fields = ['dni','nombre', 'apellido', 'genero', 'email', 'monto']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not (7 <= len(str(dni)) <= 8):
            raise ValidationError('El DNI debe tener entre 7 y 8 caracteres.')
        return dni

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(caracter.isdigit() for caracter in nombre):
            raise ValidationError('El nombre no puede contener números.')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if any(caracter.isdigit() for caracter in apellido):
            raise ValidationError('El apellido no puede contener números.')
        return apellido
