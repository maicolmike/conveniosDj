from django.contrib import admin
from django.urls import path
from . import views
from users.views import login_view,logout_view,register,usersList,CambiarClave,UserUpdateView,UserUdpateClave,UserDelete,recuperar_clave
from consulta.views import consulta

urlpatterns = [
    path('admin/', admin.site.urls),
    #agregadas por el usuario
    path('',views.index, name='index'),
    path('users/login', login_view, name='login'),
    path('users/logout', logout_view, name='logout'),
    path('users/registro',register, name='register'),
    path('users/listadoUsuarios',usersList, name='usersList'),
    path('users/cambiarClave', CambiarClave, name='CambiarClave'),
    path('users/editar', UserUpdateView, name='updateusuarios'),
    path('users/editarClave', UserUdpateClave, name='updateusuariosClave'),
    path('users/eliminarUsuarios', UserDelete, name='deleteusuarios'),
    path('users/recuperarClave', recuperar_clave, name='recuperar_clave'),
    path('consulta/consulta', consulta, name='consulta'),
]
