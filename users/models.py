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

# Modelo de Producto de Madera
class ProductoMadera(models.Model):
    especie = models.CharField(max_length=100)
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    espesor = models.DecimalField(max_digits=5, decimal_places=2)
    largo = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad = models.PositiveIntegerField()

    volumen = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_barraca = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)

    class Meta:
        unique_together = ('especie', 'ancho', 'espesor', 'largo', 'sucursal')

    def save(self, *args, **kwargs):
        self.volumen = (self.ancho * self.espesor * self.largo * self.cantidad) / 12
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.especie} - {self.ancho}x{self.espesor}x{self.largo} ({self.sucursal})'

# Venta
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.vendedor and not self.sucursal:
            self.sucursal = self.vendedor.get_sucursal()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Venta #{self.id} - {self.fecha.strftime("%Y-%m-%d")}'



class DetalleVentaMadera(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(ProductoMadera, on_delete=models.PROTECT)
    cantidad_vendida = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Validar stock
        if self.producto.cantidad < self.cantidad_vendida:
            raise ValueError(f"Stock insuficiente: solo hay {self.producto.cantidad} unidades disponibles.")

        # Calcular subtotal
        self.subtotal = self.cantidad_vendida * self.precio_unitario

        # Descontar cantidad y actualizar volumen
        self.producto.cantidad -= self.cantidad_vendida
        self.producto.save()  # Esto actualiza el volumen automáticamente

        super().save(*args, **kwargs)

class FacturaRecibo(models.Model):
    TIPO_CHOICES = (
        ('factura', 'Factura'),
        ('recibo', 'Recibo'),
    )

    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='comprobante')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    nombre_cliente = models.CharField(max_length=100)
    ci_nit = models.CharField(max_length=30)

    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.tipo.capitalize()} - {self.venta.id} - {self.nombre_cliente}'

    class Meta:
        verbose_name = 'Factura o Recibo'
        verbose_name_plural = 'Facturas o Recibos'
