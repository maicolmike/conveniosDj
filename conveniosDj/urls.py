from django.contrib import admin
from django.urls import path
from . import views
from users.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #agregadas por el usuario
    path('',views.index, name='index'),
    path('users/login', login_view, name='login'),
]
