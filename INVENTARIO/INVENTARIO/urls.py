"""INVENTARIO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myinventario.views import *
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iniciar_sesion, name='login'),
    path('index/',inventario, name="index"),
    path('logout/', logoutView, name='logout'),
    path('proveedores/', proveedores, name="proveedores"),
    path('registro/',registro,name="registro"),
    path('dashboard/',dashboard,name="dashboard"),
    path('productos/',productos,name="productos"),
    path('descuentoProductos/',descuentoProductos,name="decuentoProductos"),
    path('agregarCategoria/',agregarCategoria,name="agregarCategoria"),
    path('agregar_categoria/', agregar_categoria, name='agregar_categoria'),
    path('agregarProducto/', agregarProducto, name='agregarProducto'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('agregar_proveedor/',agregar_proveedor, name='agregar_proveedor'),
    path('eliminar_proveedor/<int:id>/', eliminar_proveedor, name='eliminar_proveedor')
]
