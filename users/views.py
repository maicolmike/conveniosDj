from django.shortcuts import render,redirect,get_object_or_404
from .models import User
from .forms import LoginUser,RegistroUsuario,CambiarClaveForm,LoginUserRecuperarClave
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.decorators import login_required # vista basada en funciones que no permita acceder a paginas donde no se ha logeado
import string
import random
#trabajar en segundo plano,
from threading import Thread # Importamos la clase Thread para ejecutar tareas en segundo plano (sin bloquear la app)
# Importamos las clases necesarias para enviar correos con formato HTML
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string #Renderiza la plantilla HTML con los datos necesarios.
# Convierte el mensaje HTML a texto plano.
from django.utils.html import strip_tags 


# -------------------------------------------------------------
# 📨 Clase EmailThread: se encarga de enviar el correo en un hilo aparte
# -------------------------------------------------------------
class EmailThread(Thread):
    # El método __init__ inicializa las variables necesarias para el envío
    def __init__(self, subject, body, from_email, to_email):
        self.subject = subject        # Asunto del correo
        self.body = body              # Cuerpo del correo (en formato HTML)
        self.from_email = from_email  # Dirección del remitente
        self.to_email = to_email      # Dirección del destinatario
        Thread.__init__(self)         # Inicializamos la clase padre Thread

    # El método run() se ejecuta cuando se llama a .start() sobre el hilo
    def run(self):
        # Creamos el objeto de correo
        msg = EmailMultiAlternatives(
            subject=self.subject,      # Asunto del correo
            body='',                   # Cuerpo de texto plano (dejamos vacío)
            from_email=self.from_email,# Dirección del remitente
            to=[self.to_email]         # Lista con los destinatarios
        )

        # Adjuntamos el cuerpo HTML como contenido alternativo
        msg.attach_alternative(self.body, "text/html")

        # Enviamos el correo
        msg.send()


# -------------------------------------------------------------
# 💌 Función: enviar_correo_bienvenida
# Envía un correo HTML al nuevo usuario con sus credenciales
# -------------------------------------------------------------
def enviar_correo_bienvenida(user, password, email):
    """Envía un correo al nuevo usuario con sus credenciales."""

    # Asunto del correo
    subject = 'Cuenta creada - Convenios Cootep'

    # Correo del remitente (usa el valor configurado en settings.DEFAULT_FROM_EMAIL)
    # El formato "nombre <correo>" hace que el correo se vea más profesional
    from_email = "servicio de notificación <{}>".format(settings.DEFAULT_FROM_EMAIL)

    # Dirección de destino (correo del usuario creado)
    to_email = email

    # Renderizamos el HTML de la plantilla con los datos personalizados del usuario
    html_content = render_to_string('emails/usuario_creado.html', {
        'nombres': user.first_name,   # Nombre del usuario
        'username': user.username,    # Nombre de usuario (login)
        'password': password,         # Contraseña (la que se asignó al crear la cuenta)
    })

    # Creamos un hilo (EmailThread) para enviar el correo sin bloquear la respuesta del servidor
    # Esto permite que Django siga ejecutándose mientras el correo se envía en segundo plano
    EmailThread(subject, html_content, from_email, to_email).start()


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
        'title': "Login convenios Cootep",
        'form': form
    })

#Cerrar de sesion login
@login_required(login_url='login') 
def logout_view(request):
    logout(request)
    messages.error(request,'Sesion cerrada')
    #messages.success(request,'Sesion cerrada')
    return redirect('login')

# Importante: solo los usuarios autenticados pueden acceder a esta vista
@login_required(login_url='login')    
def register(request):
    # Se crea una instancia del formulario RegistroUsuario. Si el método es POST, se llenará con los datos enviados.Si no, se mostrará vacío en pantalla.
    form = RegistroUsuario(request.POST or None)

    # Verificamos si el formulario fue enviado y es válido
    if request.method == 'POST' and form.is_valid():

        # Guardamos el usuario con el método save() definido en el formulario (este método crea un nuevo usuario en la base de datos)
        user = form.save()

        # Si el usuario se guardó correctamente
        if user:
            # Verificamos el tipo de usuario seleccionado en el formulario '1' = administrador, '2' = cliente
            if form.cleaned_data['is_superuser'] == '1':
                # Si es administrador, le damos permisos de staff y superusuario
                user.is_staff = True
                user.is_superuser = True

            # Guardamos nuevamente el usuario con los permisos asignados
            user.save()

            # Obtenemos la contraseña y el correo electrónico del formulario
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # Llamamos a la función que envía el correo de bienvenida con las credenciales
            enviar_correo_bienvenida(user, password, email)

            # Mostramos un mensaje en la interfaz indicando que todo salió bien
            messages.success(request, 'Usuario creado y correo enviado exitosamente.')

            # Redirigimos nuevamente a la misma página (por ejemplo, para registrar otro usuario)
            return redirect('register')

    # Si el método no es POST o el formulario tiene errores, renderizamos la página del formulario
    return render(request, 'users/register.html', {
        'form': form,       # Pasamos el formulario al template para mostrarlo
        'title': "Registro" # Título que se puede usar en la plantilla HTML
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
        first_name = request.POST.get('first_name')
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
        user.first_name = first_name
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

# esta funcion sirve para eliminar los usuarios que se obtienen de la vista listar usuarios
# esta asociada a los siguiente template/users-listUsers.html mesa_ayuda/mesa_ayuda/urls.py  path('users/eliminarUsuarios', UserDelete, name='deleteusuarios'),
@login_required(login_url='login')    
def UserDelete(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        
        # Busca el usuario en la base de datos por su ID
        try:
            user = User.objects.get(id=user_id)

            # Elimina el usuario de la base de datos
            user.delete()

        except User.DoesNotExist:
            resultado = "El usuario no existe."

        # Redirecciona a la lista de usuarios después de eliminar
        #time.sleep(1.5) #funcion para que se demore en redireccionar
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('usersList')

# generar clave automatica   
def generate_random_password():
    # Define un conjunto de caracteres que incluye letras (mayúsculas y minúsculas), dígitos y algunos caracteres especiales.
    characters = string.ascii_letters + string.digits + "*#$&!?"
    
    # Genera una contraseña aleatoria de 6 caracteres eligiendo aleatoriamente de los caracteres definidos.
    return ''.join(random.SystemRandom().choice(characters) for _ in range(6))

# recuperar clave  
def recuperar_clave(request):
    # Verifica si la solicitud es de tipo POST (es decir, si se ha enviado el formulario).
    if request.method == 'POST':
        # Crea una instancia del formulario con los datos enviados.
        form = LoginUserRecuperarClave(request.POST)
        
        # Verifica si el formulario es válido.
        if form.is_valid():
            # Obtiene el nombre de usuario ingresado en el formulario.
            username = form.cleaned_data['username']
            try:
                # Intenta obtener al usuario de la base de datos por su nombre de usuario.
                user = User.objects.get(username=username)
                
                # Genera una nueva contraseña aleatoria.
                new_password = generate_random_password()
                
                # Establece la nueva contraseña para el usuario.
                user.set_password(new_password)
                
                # Guarda los cambios en la base de datos.
                user.save()

                # Envía la nueva contraseña al correo electrónico del usuario utilizando un hilo separado para no bloquear la ejecución.
                Thread(target=send_password_email, args=(user, new_password)).start()

                # Muestra un mensaje de éxito al usuario.
                messages.success(request, f'Se ha enviado un correo para recuperar su clave.')
                
                # Redirige al usuario a la página de inicio de sesión.
                return redirect('login')
            except User.DoesNotExist:
                # Si el usuario no existe, muestra un mensaje de error.
                #messages.error(request, 'Error: El usuario no existe.')
                messages.success(request, f'Se ha enviado un correo para recuperar su clave.')
                 # Redirige al usuario a la página de inicio de sesión.
                return redirect('login')
        else:
            # Si el formulario no es válido, muestra un mensaje de error.
            messages.error(request, 'Formulario inválido.')
    else:
        # Si la solicitud no es de tipo POST, simplemente crea un formulario vacío.
        form = LoginUserRecuperarClave()

    # Renderiza la plantilla recuperarClave.html con el formulario.
    return render(request, 'users/recuperarClave.html', {
        'title': "Recuperar clave",
        'form': form,
    })

def send_password_email(user, new_password):
    # Asunto del correo electrónico.
    subject = 'Recuperación de Contraseña'
    
    # Renderiza la plantilla HTML con los datos necesarios.
    html_message = render_to_string('emails/restablecerclave.html', {'username': user.username, 'nombres': user.first_name,'new_password': new_password})
    
    # Convierte el mensaje HTML a texto plano.
    plain_message = strip_tags(html_message)
    
    # Dirección de correo electrónico del remitente personalizada.
    from_email = "servicio de notificación <{}>".format(settings.DEFAULT_FROM_EMAIL)
    
    # Lista de destinatarios.
    recipient_list = [user.email]
    
    # Envía el correo electrónico con el asunto, mensaje en texto plano, mensaje HTML, remitente y lista de destinatarios.
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)