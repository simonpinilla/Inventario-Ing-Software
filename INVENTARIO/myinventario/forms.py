from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'card__input'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'card__input'}))

# class RegistroForm(forms.ModelForm):
#     contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'card__input'}))

#     class Meta:
#         model = MiUsuario
#         fields = ['usuario', 'correo', 'contraseña']
#         widgets = {
#             'usuario': forms.TextInput(attrs={'class': 'card__input'}),
#             'correo': forms.EmailInput(attrs={'class': 'card__input'}),

class MiUsuarioCreationForm(UserCreationForm):
    class Meta:
        model = MiUsuario
        fields = ('usuario', 'correo',)  # Agrega los campos de tu modelo aquí

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['usuario'].widget.attrs.update({'class': 'form-control'})
        self.fields['correo'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        
        
        # Eliminar los mensajes de validación de contraseña
        self.fields['password1'].help_text = None
        self.fields['password1'].validators = []
        self.fields['password2'].help_text = None
        self.fields['password2'].validators = []

    def save(self, commit=True):
        user = super().save(commit=False)
        # Realiza cualquier manipulación adicional en el modelo aquí si es necesario
        if commit:
            user.save()
        return user
