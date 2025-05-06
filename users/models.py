from django.db import models
from django.contrib.auth.hashers import make_password

# Modelo de Sucursales
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# Modelo de Roles
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# Modelo de Permisos
class Permiso(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# Modelo de Usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    ci = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    imagen_url = models.URLField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

# Relación Usuario ↔ Rol ↔ Sucursal
class UsuarioRolSucursal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'rol', 'sucursal')

    def __str__(self):
        return f'{self.usuario} - {self.rol} - {self.sucursal}'

# Relación Rol ↔ Permiso
class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')

    def __str__(self):
        return f'{self.rol} - {self.permiso}'


# Modelo de Autorizaciones para el usuario forestal

# Usuario forestal
class UsuarioForestal(models.Model):
    nombre = models.CharField(max_length=100)
    ci = models.CharField(max_length=20)
    comunidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

# Transporte
class Transporte(models.Model):
    placa = models.CharField(max_length=20)
    nombre_conductor = models.CharField(max_length=100)
    ci_conductor = models.CharField(max_length=20)
    licencia = models.CharField(max_length=50)

    def __str__(self):
        return self.placa

# Romaneo
class Romaneo(models.Model):
    fecha = models.DateField()
    usuario_forestal = models.ForeignKey(UsuarioForestal, on_delete=models.CASCADE)
    transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Romaneo {self.id} - {self.fecha}"

# Inventario total actual
class Inventario(models.Model):
    especie = models.CharField(max_length=100)
    ancho = models.FloatField()
    espesor = models.FloatField()
    largo = models.FloatField()
    cantidad_total = models.FloatField(default=0)
    volumen_total = models.FloatField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('especie', 'ancho', 'espesor', 'largo')

    def __str__(self):
        return f"{self.especie} {self.ancho}x{self.espesor}x{self.largo}"

# DetalleRomaneo
class DetalleRomaneo(models.Model):
    romaneo = models.ForeignKey(Romaneo, on_delete=models.CASCADE)
    especie = models.CharField(max_length=100)
    ancho = models.FloatField(help_text="En pulgadas")
    espesor = models.FloatField(help_text="En pulgadas")
    largo = models.FloatField(help_text="En pies")  # Largo en pies
    cantidad = models.FloatField()
    volumen = models.FloatField(editable=False)  # Se calculará automáticamente
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_volumen(self):
        return (self.ancho * self.espesor * self.largo * self.cantidad) / 12

    def save(self, *args, **kwargs):
        self.volumen = self.calcular_volumen()
        super().save(*args, **kwargs)

        # Actualizar o crear en el Inventario
        inventario, creado = Inventario.objects.get_or_create(
            especie=self.especie,
            ancho=self.ancho,
            espesor=self.espesor,
            largo=self.largo,
            defaults={
                'cantidad_total': self.cantidad,
                'volumen_total': self.volumen,
                'precio_compra': self.precio_compra,
            }
        )
        if not creado:
            inventario.cantidad_total += self.cantidad
            inventario.volumen_total += self.volumen
            inventario.precio_compra = self.precio_compra
            inventario.save()


# Venta
class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    observacion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='ventas')  # 👈 Se agrega esta línea

    def __str__(self):
        return f"Venta {self.id} - {self.cliente}"

# DetalleVenta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    volumen = models.FloatField()
    precio_venta_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_venta_unitario
        super().save(*args, **kwargs)

        # Actualizar inventario al vender
        self.inventario.cantidad_total -= self.cantidad
        self.inventario.volumen_total -= self.volumen
        self.inventario.save()