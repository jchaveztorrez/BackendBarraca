from rest_framework import serializers
from .models import Sucursal, Rol, Permiso, Usuario, UsuarioRolSucursal, RolPermiso
from .models import UsuarioForestal, Transporte, Romaneo, Inventario, DetalleRomaneo, Venta, DetalleVenta

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
    usuario = UsuarioSerializer(read_only=True)
    rol = RolSerializer(read_only=True)
    sucursal = SucursalSerializer(read_only=True)

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
class UsarioForestalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioForestal
        fields = '__all__'
class TransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporte
        fields = '__all__'
class RomaneoSerializer(serializers.ModelSerializer):
    usuario_forestal = UsarioForestalSerializer(read_only=True)
    transporte = TransporteSerializer(read_only=True)

    class Meta:
        model = Romaneo
        fields = '__all__'
class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'
class DetalleRomaneoSerializer(serializers.ModelSerializer):
    romaneo = RomaneoSerializer(read_only=True)
    inventario = InventarioSerializer(read_only=True)

    class Meta:
        model = DetalleRomaneo
        fields = '__all__'
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'
class DetalleVentaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer(read_only=True)
    inventario = InventarioSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = '__all__'