# se crea el archivo views.py y se pone esto dentro
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # vista basada en funciones que no permita acceder a paginas donde no se ha logeado


@login_required(login_url='login')
def index(request):
    #return HttpResponse('Hola mundo')
    return render(request, 'index.html',{ 
        'title': "Index",
    })