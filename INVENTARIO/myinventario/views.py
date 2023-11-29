from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *

# Create your views here
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
# def registro(request):
#     if request.method == 'POST':
#         form = RegistroForm(request.POST)
#         if form.is_valid():
#             usuario_nuevo = form.save(commit=False)
#             contraseña = form.cleaned_data['contraseña']
#             usuario_nuevo.set_password(contraseña)  # Encripta la contraseña
#             usuario_nuevo.save()
#             return redirect('login')  # Redirecciona a la página de registro exitoso o a donde sea necesario
#     else:
#         form = RegistroForm()
#     return render(request, 'registro2.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = MiUsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la página de inicio de sesión o donde quieras después del registro exitoso
            return redirect('login')  # Reemplaza 'login' con el nombre de la URL de tu página de inicio de sesión
    else:
        form = MiUsuarioCreationForm()
    
    return render(request, 'registro.html', {'form': form})

 
def iniciar_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
    
        user = authenticate(request, usuario=usuario, password=password)
        print(user)
        

        if user is not None:
            print("aqui")
            login(request, user)
            # Redireccionar a una página después del inicio de sesión exitoso
            return redirect('index')  # Reemplaza 'nombre_de_la_vista' con el nombre de tu vista
        else:
            # Mostrar un mensaje de error en la página de inicio de sesión
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
            

    # Si el método de la solicitud no es POST o si hay errores, renderizar la plantilla de inicio de sesión.
    return render(request, 'login.html')   


