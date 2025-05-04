from django.shortcuts import render
from .models import Sucursal, Rol, Permiso, Usuario, UsuarioRolSucursal, RolPermiso
from .serializers import SucursalSerializer, RolSerializer, PermisoSerializer, UsuarioSerializer, UsuarioRolSucursalSerializer, RolPermisoSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import generics 

# Create your views here.
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    """ permission_classes = [permissions.IsAuthenticated] """
   
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtiene la instancia de la sucursal a eliminar
        instance.delete()  # Elimina la sucursal de la base de datos
        return Response({'status': 'sucursal deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({'status': 'permiso deactivated'}, status=status.HTTP_204_NO_CONTENT)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class UsuarioRolSucursalViewSet(viewsets.ModelViewSet):
    queryset = UsuarioRolSucursal.objects.all()
    serializer_class = UsuarioRolSucursalSerializer

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario')
        rol_id = request.data.get('rol')
        sucursal_id = request.data.get('sucursal')

        if UsuarioRolSucursal.objects.filter(usuario_id=usuario_id, rol_id=rol_id, sucursal_id=sucursal_id).exists():
            return Response({'error': ['El usuario ya tiene ese rol asignado en esa sucursal']},status=status.HTTP_400_BAD_REQUEST)

        instancia = UsuarioRolSucursal.objects.create(usuario_id=usuario_id, rol_id=rol_id, sucursal_id=sucursal_id)

        return Response(UsuarioRolSucursalSerializer(instancia).data,status=status.HTTP_201_CREATED )

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        usuario_id = request.data.get('usuario')
        rol_id = request.data.get('rol')
        sucursal_id = request.data.get('sucursal')

        # Validar si existe otra relación con los mismos datos
        existe = UsuarioRolSucursal.objects.filter(usuario_id=usuario_id, rol_id=rol_id, sucursal_id=sucursal_id).exclude(id=instance.id).exists()

        if existe:
            return Response({'error': ['Ya existe esa asignación para otro registro']}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar los campos
        instance.usuario_id = usuario_id
        instance.rol_id = rol_id
        instance.sucursal_id = sucursal_id
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # Elimina el objeto de la base de datos
        return Response({'status': 'usuario rol sucursal eliminado'}, status=status.HTTP_204_NO_CONTENT)
   
class RolPermisoViewSet(viewsets.ModelViewSet):
    queryset = RolPermiso.objects.all()
    serializer_class = RolPermisoSerializer

    def create(self, request, *args, **kwargs):
        rol_id = request.data.get('rol')
        permiso_id = request.data.get('permiso')

        if RolPermiso.objects.filter(rol_id=rol_id, permiso_id=permiso_id).exists():
            return Response({'error': ['Ya existe esta relación rol-permiso']}, status=status.HTTP_400_BAD_REQUEST)

        instancia = RolPermiso.objects.create(rol_id=rol_id, permiso_id=permiso_id)

        return Response(RolPermisoSerializer(instancia).data, status=status.HTTP_201_CREATED)

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        rol_id = request.data.get('rol')
        permiso_id = request.data.get('permiso')
        # Validar si existe otra relación con los mismos datos
        existe = RolPermiso.objects.filter(rol_id=rol_id, permiso_id=permiso_id).exclude(id=instance.id).exists()
        
        if existe:
            return Response({'error': ['Ya existe esa asignación para otro registro']}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar los campos
        instance.rol_id = rol_id
        instance.permiso_id = permiso_id
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    





class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            usuario = Usuario.objects.get(correo=request.data['correo'])
            if check_password(request.data['password'], usuario.password):
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'usuario': UsuarioSerializer(usuario).data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            usuario = request.user
            if check_password(request.data['old_password'], usuario.password):
                usuario.password = make_password(request.data['new_password'])
                usuario.save()
                return Response({'status': 'Password changed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

