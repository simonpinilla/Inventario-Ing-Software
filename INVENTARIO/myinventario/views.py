from django.shortcuts import render, redirect
from .models import *
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
    return render(request, 'prove.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def productos(request):
    return render(request, 'productos.html')

def descuentoProductos(request):
    return render(request, 'descuentoProductos.html')

def agregarCategoria(request):
    return render(request, 'agregarCategoria.html')

def agregarProducto(request):
    categorias = Categoria.objects.all()
    return render(request, 'agregarProducto.html', {'categorias': categorias})


def agregar_categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        descripcion_categoria = request.POST.get('descripcion_categoria')

        print(f'Nombre de la categoría: {nombre_categoria}')
        print(f'Descripción de la categoría: {descripcion_categoria}')
        print("aqui")

        # Crea y guarda la nueva categoría
        nueva_categoria = Categoria(nombre=nombre_categoria, descripcion=descripcion_categoria)
        nueva_categoria.save()

        return redirect('dashboard')  # Redirige a la vista deseada después de agregar la categoría

    return render(request, 'agregarCategoria.html')  # Renderiza la plantilla del formulario


def agregar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        descripcion_producto = request.POST.get('descripcion_producto')
        cantidad_producto = request.POST.get('cantidad_producto')
        precio_producto = request.POST.get('precio_producto')
        categoria_id = request.POST.get('categoria_producto')

        # Obtener la categoría seleccionada
        categoria_seleccionada = Categoria.objects.get(id=categoria_id)

        # Crear y guardar el nuevo producto con la categoría seleccionada
        nuevo_producto = Producto(
            nombre=nombre_producto,
            descripcion=descripcion_producto,
            cantidad=cantidad_producto,
            precio=precio_producto,
            categoria_id=categoria_seleccionada
        )
        nuevo_producto.save()

        return redirect('productos')  # Redirige a la vista deseada después de agregar el producto

    categorias = Categoria.objects.all()  # Obtener todas las categorías disponibles
    return render(request, 'agregarProducto', {'categorias': categorias})

    

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
            return redirect('dashboard')  # Reemplaza 'nombre_de_la_vista' con el nombre de tu vista
        else:
            # Mostrar un mensaje de error en la página de inicio de sesión
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
            

    # Si el método de la solicitud no es POST o si hay errores, renderizar la plantilla de inicio de sesión.
    return render(request, 'login.html')   


