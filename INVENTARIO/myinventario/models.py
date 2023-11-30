from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.admin.models import LogEntry

class MiUsuarioManager(BaseUserManager):
    def create_user(self, usuario, correo, password=None):
        # Crea y guarda un usuario con los campos proporcionados
        if not usuario:
            raise ValueError('El usuario es obligatorio')
        if not correo:
            raise ValueError('El correo es obligatorio')

        user = self.model(
            usuario=usuario,
            correo=self.normalize_email(correo),
        )
        user.set_password(password)  # Encripta la contraseña antes de guardarla
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, correo, password):
        user = self.create_user(
            usuario=usuario,
            correo=correo,
            password=password,
        )
        
        user.save(using=self._db)
        return user

class MiUsuario(AbstractBaseUser):
    usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)

    
    # Otros campos personalizados si es necesario

    objects = MiUsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['correo']

    def __str__(self):
        return self.usuario

    def has_perm(self, perm, obj=None):
        return self.es_administrador

    def has_module_perms(self, app_label):
        return self.es_administrador
    

class Orden(models.Model):
    fecha = models.DateField()
    id_usuario = models.ForeignKey(MiUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} - Fecha: {self.fecha} - Usuario: {self.id_usuario}"
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.nombre}"



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    precio = models.CharField(max_length=20)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor_id = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    

    def __str__(self):
        return f"Proveedor: {self.nombre}"


class DetalleOrden(models.Model):
    cantidad_producto = models.IntegerField()
    orden_id = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)

    

    def __str__(self):
        return f"DetalleOrden: {self.cantidad_producto}"
    

