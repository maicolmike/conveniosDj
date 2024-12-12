from django import forms
#from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginUser(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50,label='Usuario',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'username',
                                                             'placeholder': 'Username'}))
    password = forms.CharField(required=True,label='Contraseña',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'id': 'password',
                                                             'placeholder': 'Password'}))

class RegistroUsuario(forms.Form):
    
    username = forms.CharField(required=True, min_length=4, max_length=50,label='Usuario',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'username',
                                                             'placeholder': 'Username'}))
    first_name = forms.CharField(required=True, min_length=4, max_length=50,label='nombre',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'nombre',
                                                             'placeholder': 'nombre'}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'id': 'password',
                                                             'placeholder': 'Password'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                             'id': 'email',
                                                             'placeholder': 'Email'}))
    TIPOS_USUARIO = [
        ('', ''),
        (1, 'Administrador'),
        (2, 'Cliente'),
    ]
    
    is_superuser = forms.ChoiceField(label='Tipo de usuario',required=True,choices=TIPOS_USUARIO,
        widget=forms.Select(attrs={'class': 'form-control','id': 'tipousuario'})  # Personaliza el widget aquí
    )
        
    #usuario no se repita y no genere error
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists() :
            raise forms.ValidationError("el usuario ya se encuentra creado")
        
        return username

    #Guardar  
    def save(self):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        user = User.objects.create_user(username=username, first_name=first_name, email=email, password=password)
        
        return user

# formulario con clases
class CambiarClaveForm(forms.Form):
    
    passwordActual = forms.CharField(label= 'Contraseña actual',required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'id': 'password',
                                                             'placeholder': 'Contraseña actual'}))
    passwordNew = forms.CharField(label= 'Contraseña nueva',required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'id': 'passwordNew',
                                                             'placeholder': 'Contraseña nueva'}))
    passwordNewConfirm = forms.CharField(label= 'Confirmar Contraseña',
                                required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'id': 'passwordNewConfirm',
                                                             'placeholder': 'Confirmar contraseña'}))

class LoginUserRecuperarClave(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50,label='Usuario',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'username',
                                                             'placeholder': 'Usuario'}))