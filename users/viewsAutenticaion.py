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
    

    """ def get_queryset(self):
        return self.queryset.filter(estado=True)

    @action(detail=False, methods=['get'])
    def inactive(self, request):
        inactive_sucursales = self.queryset.filter(estado=False)
        serializer = self.get_serializer(inactive_sucursales, many=True)
        return Response(serializer.data) """
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
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
        instance = self.get_object()
        instance.estado = False
        instance.save()
        return Response({'status': 'rol deactivated'}, status=status.HTTP_204_NO_CONTENT)

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
        return Response({'status': 'usuario deactivated'}, status=status.HTTP_204_NO_CONTENT)
class UsuarioRolSucursalViewSet(viewsets.ModelViewSet):
    queryset = UsuarioRolSucursal.objects.all()
    serializer_class = UsuarioRolSucursalSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        return Response({'status': 'usuario rol sucursal deactivated'}, status=status.HTTP_204_NO_CONTENT)
class RolPermisoViewSet(viewsets.ModelViewSet):
    queryset = RolPermiso.objects.all()
    serializer_class = RolPermisoSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        return Response({'status': 'rol permiso deactivated'}, status=status.HTTP_204_NO_CONTENT)
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

