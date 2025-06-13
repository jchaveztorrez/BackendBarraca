from rest_framework import serializers
from .models import Categoria, Sucursal, Rol, Permiso, Usuario, UsuarioRolSucursal, RolPermiso
from .models import ProductoMadera,Venta, DetalleVentaMadera, FacturaRecibo

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'
        
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioRolSucursalSerializer(serializers.ModelSerializer):
    
    rol = RolSerializer(read_only=True)
    sucursal = SucursalSerializer(read_only=True)
    usuario = UsuarioSerializer(read_only=True)
    class Meta:
        model = UsuarioRolSucursal
        fields = '__all__'
        
class RolPermisoSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    permiso = PermisoSerializer(read_only=True)
    class Meta:
        model = RolPermiso
        fields = '__all__'

        
""" Modelo de Autorizaciones para el usuario forestal """

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoMaderaSerializer(serializers.ModelSerializer):
    sucursal = SucursalSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta:
        model = ProductoMadera
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    vendedor = UsuarioSerializer(read_only=True)
    sucursal = SucursalSerializer(read_only=True)
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaMaderaSerializer(serializers.ModelSerializer):
    producto = ProductoMaderaSerializer(read_only=True)
    venta = VentaSerializer(read_only=True)

    class Meta:
        model = DetalleVentaMadera
        fields = '__all__'
class FacturaReciboSerializer(serializers.ModelSerializer):
    venta = VentaSerializer(read_only=True)

    class Meta:
        model = FacturaRecibo
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField(max_length=100, required=False, allow_null=True)
    password = serializers.CharField(max_length=255, required=True)  
