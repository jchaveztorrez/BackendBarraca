from rest_framework import serializers
from .models import Sucursal, Rol, Permiso, Usuario, UsuarioRolSucursal, RolPermiso


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