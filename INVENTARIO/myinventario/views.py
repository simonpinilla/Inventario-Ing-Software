from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *
from functools import reduce
from django.utils import timezone
from django.http import HttpResponseServerError
from django.http import *
from django.db import transaction



# Create your views here
def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def inventario(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def listar_orden(request):
    # Obtener todas las órdenes
    ordenes = Orden.objects.all()

    # Crear una lista para almacenar detalles asociados a cada orden
    detalles_por_orden = []

    # Iterar sobre todas las órdenes y obtener los detalles asociados
    for orden in ordenes:
        detalles = DetalleOrden.objects.filter(orden=orden)
        detalles_por_orden.append({
            'orden': orden,
            'detalles': detalles
        })

    # Pasar la información a la plantilla
    context = {
        'detalles_por_orden': detalles_por_orden
    }

    # Renderizar la plantilla y devolver la respuesta
    return render(request, 'listarOrden.html', context)


@login_required
def cuenta(request):
    usuario = request.user  # Objeto de usuario disponible para usuarios autenticados
    context = {'usuario': usuario}
    return render(request, 'listarUsuario.html', context)

@login_required
def editar_usuario(request):
    usuario = request.user
    if request.method == 'POST':
        form = MiUsuarioCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = MiUsuarioCreationForm(instance=usuario)
    return render(request, 'editarUsuario.html', {'form': form})


@login_required(login_url='login')
def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'prove.html',{"proveedores" : proveedores})

@login_required(login_url='login')
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria.html',{"categorias" : categorias})



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def productos(request):
    productos= Producto.objects.all()
    bajo_stock = reduce(lambda x, y: x or y.cantidad < 10, productos, False)
    return render(request, 'productos.html', {"productos": productos, "bajo_stock": bajo_stock})


@login_required
def detalle_orden(request):
    return render(request, 'detalleOrden.html')


@login_required
def agregarCategoria(request):
    return render(request, 'agregarCategoria.html')


@login_required
def agregarProducto(request):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'agregarProducto.html', {'categorias': categorias, 'proveedores': proveedores})


@login_required
def buscar_productos(request):
    query = request.GET.get('query', '')
    productos = Producto.objects.filter(nombre__icontains=query)
    
    if productos.exists():
        # Serialización manual a JSON
        serialized_productos = list(productos.values('id', 'nombre','cantidad','precio'))
        return JsonResponse({'productos': serialized_productos}, safe=False)
    else:
        return JsonResponse({'message': 'No se encontraron productos.'})
    
    
@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        descripcion_categoria = request.POST.get('descripcion_categoria')

        # Crea y guarda la nueva categoría
        nueva_categoria = Categoria(nombre=nombre_categoria, descripcion=descripcion_categoria)
        nueva_categoria.save()

        return redirect('categorias')  # Redirige a la vista deseada después de agregar la categoría

    return render(request, 'agregarCategoria.html')  # Renderiza la plantilla del formulario


@login_required
def procesar_orden(request):
    if request.method == 'POST':
        productos_seleccionados_ids = request.POST.getlist('productos_seleccionados_ids')
        productos_seleccionados_ids = [id for id in productos_seleccionados_ids if id != '']
        print("Productos Seleccionados IDs:", productos_seleccionados_ids)
        usuario = request.user
        nueva_orden = Orden.objects.create(fecha=timezone.now(), usuario=usuario)

        errores = []

        for producto_id in productos_seleccionados_ids:
            producto = Producto.objects.get(pk=producto_id)
            cantidad_seleccionada = request.POST.get(f'cantidad_producto_{producto_id}')

            try:
                cantidad_seleccionada = int(cantidad_seleccionada)
                if cantidad_seleccionada > 0 and producto.cantidad >= cantidad_seleccionada:
                    producto.cantidad -= cantidad_seleccionada
                    producto.save()

                    detalle = DetalleOrden.objects.create(
                        cantidad_producto=cantidad_seleccionada,
                        orden=nueva_orden,
                        producto=producto
                    )
                    detalle.save()
                else:
                    errores.append(f"No hay suficiente cantidad de {producto.nombre}.")
            except (ValueError, Producto.DoesNotExist):
                errores.append("Cantidad seleccionada no válida para el producto.")

        if not errores:
            detalles_orden = DetalleOrden.objects.filter(orden=nueva_orden).select_related('producto')
            
            # Obtener detalles con nombres de productos
            detalles_json = []
            for detalle in detalles_orden:
                producto = Producto.objects.get(pk=detalle.producto_id)
                detalle_dict = {
                    'id': detalle.id,
                    'cantidad_producto': detalle.cantidad_producto,
                    'orden_id': detalle.orden_id,
                    'producto_id': detalle.producto_id,
                    'nombre_producto': producto.nombre  # Agregar el nombre del producto al diccionario
                }
                detalles_json.append(detalle_dict)

            return JsonResponse({'detalles_orden': detalles_json})
        else:
        
            print(errores)
    return render(request, 'detalleOrden.html')



@login_required
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



@login_required
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



@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        categoria.save()
        return redirect('categorias')
    return render(request, 'editarCategoria.html', {'categoria': categoria})



@login_required
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


@login_required
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


@login_required
def eliminar_producto(request, id):
    producto = Producto.objects.get(id = id)
    producto.delete()
    return redirect('productos')


@login_required
def eliminar_proveedor(request, id):
    proveedor = Proveedor.objects.get(id = id)
    proveedor.delete()
    return redirect('proveedores')


@login_required
def eliminar_categoria(request, id):
    categorias = Categoria.objects.get(id = id)
    categorias.delete()
    return redirect('categorias')


@login_required
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

 
@login_required
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


