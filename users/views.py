from django.shortcuts import render

# Create your views here.
#Inicio de sesion login
def login_view(request):
    return render(request, 'users/login.html', {
        'title': "Login",
        
    })
