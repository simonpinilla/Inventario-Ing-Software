from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.

def loginView(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso')
                return redirect('index')  # Redirige a la página principal después del inicio de sesión
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Credenciales incorrectas. Por favor, inténtelo de nuevo.'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Credenciales incorrectas. Por favor, inténtelo de nuevo.'})
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def inventario(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def proveedores(request):
    return render(request, 'proveedores.html')

    



# funcion para crear el usuario   user = admin,  password = 344321
def registrar(request):
    if request.method == "GET":
        return render(request, "registrar.html", {
            "form": UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_superuser(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse('Usuario creado correctamente')
            except:
                return HttpResponse('usuario ya existe')
        return HttpResponse('Password no coinsiden')


    


