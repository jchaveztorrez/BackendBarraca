from django.shortcuts import render
from .models import Categoria, DetalleVentaMadera, FacturaRecibo, ProductoMadera, Sucursal, Rol, Permiso, Usuario, UsuarioRolSucursal, RolPermiso, Venta
from .serializers import CategoriaSerializer, DetalleVentaMaderaSerializer, FacturaReciboSerializer, ProductoMaderaSerializer, SucursalSerializer, RolSerializer, PermisoSerializer, UsuarioSerializer, UsuarioRolSucursalSerializer, RolPermisoSerializer, VentaSerializer
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
    

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProductoMaderaViewSet(viewsets.ModelViewSet):
    queryset = ProductoMadera.objects.all()
    serializer_class = ProductoMaderaSerializer

    def create(self, request, *args, **kwargs):
        data = {key: request.data.get(key) for key in [
            'especie', 'ancho', 'espesor', 'largo', 'cantidad',
            'precio_compra', 'precio_barraca', 'precio_venta'
        ]}

        categoria_id = request.data.get('categoria')
        try:
            data['categoria'] = Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            return Response({"error": "La categoría especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)

        sucursal_id = request.data.get('sucursal')
        try:
            data['sucursal'] = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            return Response({"error": "La sucursal especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)

        if ProductoMadera.objects.filter(
            especie=data['especie'],
            ancho=data['ancho'],
            espesor=data['espesor'],
            largo=data['largo'],
            sucursal=data['sucursal'],
            categoria=data['categoria']  # <-- incluida en validación
        ).exists():
            return Response(
                {'detail': 'Ya existe un producto con esa especie, dimensiones, sucursal y categoría.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        producto_madera = ProductoMadera.objects.create(**data)
        return Response(ProductoMaderaSerializer(producto_madera).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        categoria_id = data.get('categoria')
        if categoria_id:
            try:
                instance.categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                return Response(
                    {"error": "La categoría especificada no existe."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        sucursal_id = data.get('sucursal')
        if sucursal_id:
            try:
                instance.sucursal = Sucursal.objects.get(id=sucursal_id)
            except Sucursal.DoesNotExist:
                return Response(
                    {"error": "La sucursal especificada no existe."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        for field in [
            'especie', 'ancho', 'espesor', 'largo',
            'cantidad', 'precio_compra', 'precio_barraca', 'precio_venta'
        ]:
            if field in data:
                setattr(instance, field, data[field])

        if ProductoMadera.objects.exclude(pk=instance.pk).filter(
            especie=instance.especie,
            ancho=instance.ancho,
            espesor=instance.espesor,
            largo=instance.largo,
            sucursal=instance.sucursal,
            categoria=instance.categoria  # <-- incluida en validación
        ).exists():
            return Response(
                {'detail': 'Ya existe otro producto con esa especie, dimensiones, sucursal y categoría.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class VentasViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def create(self, request, *args, **kwargs):
        vendedor_id = request.data.get('vendedor_id')
        sucursal_id = request.data.get('sucursal_id')
        total = request.data.get('total', 0)

        if not vendedor_id or not sucursal_id:
            return Response({"error": "Se requiere el vendedor y la sucursal"}, status=status.HTTP_400_BAD_REQUEST)

        venta = Venta.objects.create(
            vendedor_id=vendedor_id,
            sucursal_id=sucursal_id,
            total=total
        )

        serializer = self.get_serializer(venta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DetallesVentasViewSet(viewsets.ModelViewSet):
    queryset = DetalleVentaMadera.objects.all()
    serializer_class = DetalleVentaMaderaSerializer

    def create(self, request, *args, **kwargs):
           try:
               venta_id = request.data.get('venta')
               producto_id = request.data.get('producto')
               cantidad_vendida = int(request.data.get('cantidad_vendida'))
               precio_unitario = float(request.data.get('precio_unitario'))

               producto = ProductoMadera.objects.get(pk=producto_id)

               if producto.cantidad < cantidad_vendida:
                   return Response({"error": f"Stock insuficiente. Disponible: {producto.cantidad}"}, status=status.HTTP_400_BAD_REQUEST)

               detalle = DetalleVentaMadera.objects.create(
                   venta_id=venta_id,
                   producto=producto,
                   cantidad_vendida=cantidad_vendida,
                   precio_unitario=precio_unitario
               )



               serializer = self.get_serializer(detalle)
               return Response(serializer.data, status=status.HTTP_201_CREATED)

           except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FacturaReciboViewSet(viewsets.ModelViewSet):
    queryset = FacturaRecibo.objects.all()
    serializer_class = FacturaReciboSerializer

    def create(self, request, *args, **kwargs):
        venta_id = request.data.get('venta')
        if not venta_id:
            return Response({"error": "Se requiere el ID de la venta"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            venta = Venta.objects.get(pk=venta_id)
        except Venta.DoesNotExist:
            return Response({"error": "La venta especificada no existe."}, status=status.HTTP_404_NOT_FOUND)

        factura_recibo = FacturaRecibo.objects.create(venta=venta)
        serializer = self.get_serializer(factura_recibo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

