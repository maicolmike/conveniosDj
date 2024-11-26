from django.shortcuts import render
from .models import User
from .forms import LoginUser,RegistroUsuario,CambiarClaveForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required # vista basada en funciones que no permita acceder a paginas donde no se ha logeado
from django.contrib.auth import update_session_auth_hash


# Create your views here.
#Inicio de sesion login
def login_view(request):
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.success(request, 'Bienvenido {}'.format(user.username))
                messages.success(request, 'Bienvenido {}'.format(user.username))
                return redirect('index')  # Redirige al usuario a la página de inicio
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginUser()  # Crea un formulario vacío si la solicitud no es POST
    
    # Si el usuario ya está autenticado, redirige a la página de inicio
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'users/login.html', {
        'title': "Login",
        'form': form
    })

#Cerrar de sesion login
@login_required(login_url='login') 
def logout_view(request):
    logout(request)
    messages.error(request,'Sesion cerrada')
    #messages.success(request,'Sesion cerrada')
    return redirect('login')

#Registrar usuario
@login_required(login_url='login')    
def register(request):
    
    form = RegistroUsuario(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save() #save () se encuentra en el archivo forms.py
        if user:
            if form.cleaned_data['is_superuser'] == '1': #El campo en el formulario html es 1
                #otorgar permisos de administrador
                user.is_staff = True
                user.is_superuser = True
            user.save()
            messages.success(request, 'usuario creado')
            return redirect('register')
    
    return render(request, 'users/register.html', {
        'form': form,
        'title': "Registro",
        })

#Listar usuarios
@login_required(login_url='login')
def usersList(request):
    #return HttpResponse('Hola mundo')
    lista_usuarios = User.objects.all()
    return render(request, 'users/listUsers.html',{ 
        'title': "Listado Usuarios",
        'lista_usuarios': lista_usuarios,
    })

@login_required(login_url='login')    
def CambiarClave(request):
    
    form = CambiarClaveForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        password_actual = form.cleaned_data['passwordActual']
        password_nueva = form.cleaned_data['passwordNew']
        confirmar_password = form.cleaned_data['passwordNewConfirm']

        # Validar que la contraseña actual sea correcta
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return render(request, 'users/cambiarClave.html', {'form': form, 'title': 'Cambiar clave'})
        
        # Validar que la contraseña actual sea diferente de la nueva
        if password_actual == password_nueva:
            messages.error(request, 'La nueva contraseña debe ser diferente de la contraseña actual.')
            return render(request, 'users/cambiarClave.html', {'form': form, 'title': 'Cambiar clave'})
        
        # Validar que la nueva contraseña y la confirmación coincidan
        if password_nueva != confirmar_password:
            messages.error(request, 'La nueva contraseña y confirmacion de contraseña no coinciden.')
            return render(request, 'users/cambiarClave.html', {'form': form, 'title': 'Cambiar clave'})

        # Cambiar la contraseña del usuario
        request.user.set_password(password_nueva)   #request.user es específico para interactuar con el usuario que ha iniciado sesión en ese momento, 
        request.user.save()

        # Actualizar la sesión del usuario para evitar cerrar sesión después de cambiar la contraseña
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Contraseña cambiada exitosamente.')

    return render(request, 'users/cambiarClave.html', {'form': form, 'title': 'Cambiar clave'})

# esta funcion sirve para editar los usuarios que se obtienen de la vista listar usuarios
# esta asociada a los siguiente: template/users/listUsers.html     mesa_ayuda/mesa_ayuda/urls.py path('users/editar', UserUpdateView, name='updateusuarios'),
# esta funcion esta sirviendo con modalEdtiar usuarios
@login_required(login_url='login')
def UserUpdateView(request):
    """
    Vista para actualizar la información de un usuario existente.
    """
    if request.method == 'POST':
        # Obtiene los datos del formulario
        user_id = request.POST.get('id')
        username = request.POST.get('username')
        email = request.POST.get('userEmail')
        tipousuario = request.POST.get('tipousuario')
        estado = request.POST.get('estado')
        
        # Busca el usuario en la base de datos por su ID
        user = get_object_or_404(User, id=user_id)

        # Verificar si el nuevo nombre de usuario ya existe y no es el del propio usuario
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, "Error: el nombre de usuario ya existe.")
            return redirect('usersList')
        
        # Actualiza los campos con los nuevos valores
        user.username = username
        user.email = email
        user.is_superuser = tipousuario
        user.is_active = estado

        # Guarda los cambios en la base de datos
        user.save()
        messages.success(request, "Usuario actualizado exitosamente.")
        return redirect('usersList')

    return redirect('usersList')

# esta funcion sirve para actualizar la clave los usuarios que se obtienen de la vista listar usuarios
# esta asociada a los siguiente template/users/listUsers.html  mesa_ayuda/mesa_ayuda/urls.py path('users/editarClave', UserUdpateClave, name='updateusuariosClave'),
@login_required(login_url='login')    
def UserUdpateClave(request):
    
    if request.method == 'POST':
        user_id = request.POST.get('id')
        new_password = request.POST.get('passnew')

        try:
            # Obtén el usuario de la base de datos
            user = User.objects.get(id=user_id) #En contraste, si tuvieras un objeto User específico (por ejemplo, obtenido de una consulta a la base de datos), podrías hacer user.set_password(password_nueva) y user.save() para cambiar la contraseña de ese usuario en particular. Esto podría ser útil en situaciones donde estás trabajando con información específica de un usuario, independientemente de la sesión actual.

            # Establece la nueva contraseña usando set_password()
            user.set_password(new_password)

            # Guarda el usuario, lo que encripta la nueva contraseña
            user.save()
            
            # Actualizar la sesión del usuario para evitar cerrar sesión después de cambiar la contraseña
            update_session_auth_hash(request, user)
            
        except User.DoesNotExist:
            resultado = "El usuario no existe."
            
        #time.sleep(1.5) #funcion para que se demore en redireccionar
        messages.success(request, "Clave actualizada exitosamente.")
        return redirect('usersList')