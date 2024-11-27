from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # vista basada en funciones que no permita acceder a paginas donde no se ha logeado
from .forms import ConsultaAsociado

@login_required(login_url='login')
def consulta(request):
    #return HttpResponse('Hola mundo')
    form = ConsultaAsociado(request.POST or None)
    return render(request, 'consulta/consulta.html',{ 
        'title': "Consultar asociado",
        'form': form,
    })
