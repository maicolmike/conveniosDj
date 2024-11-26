from django.contrib import admin
from django.urls import path
from . import views
from users.views import login_view,logout_view,register

urlpatterns = [
    path('admin/', admin.site.urls),
    #agregadas por el usuario
    path('',views.index, name='index'),
    path('users/login', login_view, name='login'),
    path('users/logout', logout_view, name='logout'),
    path('users/registro',register, name='register'),
]
