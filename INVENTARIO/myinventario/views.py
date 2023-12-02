from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *
from functools import reduce



# Create your views here
def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def inventario(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'prove.html',{"proveedores" : proveedores})

@login_required(login_url='login')
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria.html',{"categorias" : categorias})


def dashboard(request):
    return render(request, 'dashboard.html')

def productos(request):
    productos= Producto.objects.all()
    bajo_stock = reduce(lambda x, y: x or y.cantidad < 10, productos, False)
    return render(request, 'productos.html', {"productos": productos, "bajo_stock": bajo_stock})

def agregar_orden(request):
    return render(request, 'agregarOrden.html')

def agregarCategoria(request):
    return render(request, 'agregarCategoria.html')

def agregarProducto(request):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'agregarProducto.html', {'categorias': categorias, 'proveedores': proveedores})

def buscar_productos(request):
    query = request.GET.get('query', '')
    productos = Producto.objects.filter(nombre__icontains=query)
    
    if productos.exists():
        # Serialización manual a JSON
        serialized_productos = list(productos.values('id', 'nombre','cantidad','precio'))
        return JsonResponse({'productos': serialized_productos}, safe=False)
    else:
        return JsonResponse({'message': 'No se encontraron productos.'})
def agregar_categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        descripcion_categoria = request.POST.get('descripcion_categoria')

        # Crea y guarda la nueva categoría
        nueva_categoria = Categoria(nombre=nombre_categoria, descripcion=descripcion_categoria)
        nueva_categoria.save()

        return redirect('categorias')  # Redirige a la vista deseada después de agregar la categoría

    return render(request, 'agregarCategoria.html')  # Renderiza la plantilla del formulario

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre_proveedor = request.POST.get('nombre_proveedor')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')

        proveedor = Proveedor(nombre=nombre_proveedor, telefono=telefono, direccion= direccion, ciudad=ciudad  )
        proveedor.save()
        return redirect('proveedores')
    return render(request, 'agregarProveedor.html')  


def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'POST':
        proveedor.nombre = request.POST.get('nombre')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.ciudad = request.POST.get('ciudad')
        proveedor.save()
        return redirect('proveedores')
    return render(request, 'editarProveedor.html', {'proveedor': proveedor})

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        categoria.save()
        return redirect('categorias')
    return render(request, 'editarCategoria.html', {'categoria': categoria})


def agregar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        descripcion_producto = request.POST.get('descripcion_producto')
        cantidad_producto = request.POST.get('cantidad_producto')
        precio_producto = request.POST.get('precio_producto')
        categoria_id = request.POST.get('categoria_producto')
        proveedor_id = request.POST.get('proveedor')

        categoria = Categoria.objects.get(pk=categoria_id)
        proveedor = Proveedor.objects.get(pk=proveedor_id)

        nuevo_producto = Producto(
            nombre=nombre_producto,
            descripcion=descripcion_producto,
            cantidad=cantidad_producto,
            precio=precio_producto,
            categoria=categoria,
            proveedor=proveedor
        )
        nuevo_producto.save()

        return redirect('productos')
    return render(request, 'agregarProducto')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        descripcion_producto = request.POST.get('descripcion_producto')
        cantidad_producto = request.POST.get('cantidad_producto')
        precio_producto = request.POST.get('precio_producto')
        categoria_id = request.POST.get('categoria_producto')
        proveedor_id = request.POST.get('proveedor')

        categoria = Categoria.objects.get(pk=categoria_id)
        proveedor = Proveedor.objects.get(pk=proveedor_id)
        
        producto.nombre = nombre_producto
        producto.descripcion = descripcion_producto
        producto.cantidad = cantidad_producto
        producto.precio = precio_producto
        producto.categoria_id = categoria
        producto.proveedor_id = proveedor
        producto.save()
        return redirect('productos') 
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'editarProducto.html', {'producto': producto, 'categorias': categorias, 'proveedores': proveedores})

def eliminar_producto(request, id):
    producto = Producto.objects.get(id = id)
    producto.delete()
    return redirect('productos')


def eliminar_proveedor(request, id):
    proveedor = Proveedor.objects.get(id = id)
    proveedor.delete()
    return redirect('proveedores')

def eliminar_categoria(request, id):
    categorias = Categoria.objects.get(id = id)
    categorias.delete()
    return redirect('categorias')

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


