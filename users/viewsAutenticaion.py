from django.shortcuts import render
from .models import Categoria, DetalleVentaMadera, FacturaRecibo, ProductoMadera, Sucursal, Rol, Permiso, Usuario, UsuarioRolSucursal, RolPermiso, Venta
from .serializers import CategoriaSerializer, DetalleVentaMaderaSerializer, FacturaReciboSerializer, LoginSerializer, ProductoMaderaSerializer, SucursalSerializer, RolSerializer, PermisoSerializer, UsuarioSerializer, UsuarioRolSucursalSerializer, RolPermisoSerializer, VentaSerializer
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
from django.db.models import Prefetch
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Usuario
from .serializers import UsuarioSerializer
from django.db.models import Q

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
        data = request.data.copy()

        # Subir la imagen a Cloudinary si se incluye
        if 'imagen_url' in request.FILES:
            try:
                uploaded_image = cloudinary.uploader.upload(request.FILES['imagen_url'])
                data['imagen_url'] = uploaded_image.get('url')
                print("Imagen subida correctamente:", data['imagen_url'])
            except Exception as e:
                print("Error al subir imagen a Cloudinary:", e)
                return Response({'error': 'Error al subir imagen a Cloudinary'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        # Verifica que la imagen se esté recibiendo
        print("Archivos recibidos:", request.FILES)

        # Subir nueva imagen si existe
        if 'imagen_url' in request.FILES:
            try:
                uploaded_image = cloudinary.uploader.upload(request.FILES['imagen_url'])
                data['imagen_url'] = uploaded_image.get('url')
            except Exception as e:
                return Response({'error': 'Error al subir imagen a Cloudinary'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

#si el usuario no tien asigando un rol en una sucursal, no se le permite crear un usuario rol sucursal

class UsuarioRolSucursalViewSet(viewsets.ModelViewSet):
    queryset = UsuarioRolSucursal.objects.all()
    serializer_class = UsuarioRolSucursalSerializer

    def create(self, request, *args, **kwargs):
        usuario_data = request.data.get('usuario')
        rol_data = request.data.get('rol')
        sucursal_data = request.data.get('sucursal')

        if not usuario_data or not rol_data or not sucursal_data:
            return Response({'error': 'Datos incompletos'}, status=status.HTTP_400_BAD_REQUEST)

        usuario_id = usuario_data.get('id')
        rol_id = rol_data.get('id')
        sucursal_id = sucursal_data.get('id')

        if not usuario_id or not rol_id or not sucursal_id:
            return Response({'error': 'IDs inválidos'}, status=status.HTTP_400_BAD_REQUEST)

        # Validación: ya existe la misma asignación
        if UsuarioRolSucursal.objects.filter(usuario_id=usuario_id, rol_id=rol_id, sucursal_id=sucursal_id).exists():
            return Response({'error': ['El usuario ya tiene ese rol asignado en esa sucursal']}, status=status.HTTP_400_BAD_REQUEST)

        # Validación: usuario ya tiene otro rol asignado
        if UsuarioRolSucursal.objects.filter(usuario_id=usuario_id).exclude(rol_id=rol_id).exists():
            return Response({'error': ['El usuario ya tiene un rol asignado diferente']}, status=status.HTTP_400_BAD_REQUEST)

        # Validación: usuario ya tiene otra sucursal asignada
        if UsuarioRolSucursal.objects.filter(usuario_id=usuario_id).exclude(sucursal_id=sucursal_id).exists():
            return Response({'error': ['El usuario ya tiene una sucursal asignada diferente']}, status=status.HTTP_400_BAD_REQUEST)

        instancia = UsuarioRolSucursal.objects.create(
            usuario_id=usuario_id,
            rol_id=rol_id,
            sucursal_id=sucursal_id
        )

        return Response(UsuarioRolSucursalSerializer(instancia).data, status=status.HTTP_201_CREATED)
    
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

        nombre_normalizado = request.data.get('nombre', '').strip().lower()
        if Categoria.objects.filter(nombre__iexact=nombre_normalizado).exists():
            raise ValidationError({'nombre': 'Ya existe una categoría con ese nombre (sin importar mayúsculas/minúsculas).'})

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()

        nuevo_nombre = request.data.get('nombre', '').strip().lower()

        # Evitar conflictos con otras categorías (distintas del actual ID)
        if Categoria.objects.filter(
            ~Q(id=instance.id),
            nombre__iexact=nuevo_nombre
        ).exists():
            raise ValidationError({'nombre': 'Ya existe una categoría con ese nombre (sin importar mayúsculas/minúsculas).'})

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
        venta_data = request.data.get('venta')
        venta_id = venta_data.get('id') if isinstance(venta_data, dict) else venta_data

        if not venta_id:
            return Response({"error": "Se requiere el ID de la venta"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            venta = Venta.objects.get(pk=venta_id)
        except Venta.DoesNotExist:
            return Response({"error": "La venta especificada no existe."}, status=status.HTTP_404_NOT_FOUND)

        tipo = request.data.get('tipo')
        nombre_cliente = request.data.get('nombre_cliente')
        ci_nit = request.data.get('ci_nit')
        total = request.data.get('total')

        if not all([tipo, nombre_cliente, ci_nit, total]):
            return Response({"error": "Faltan campos obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            factura_recibo = FacturaRecibo.objects.create(
                venta=venta,
                tipo=tipo,
                nombre_cliente=nombre_cliente,
                ci_nit=ci_nit,
                total=total
            )
            serializer = self.get_serializer(factura_recibo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Ocurrió un error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#si el usuario no tien asigando un rol en una sucursal, no se le permite accesder al sistema 
class LoginView(APIView):
    authentication_classes = []  # No autenticación requerida para login
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        # Validar datos del login
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        correo = serializer.validated_data.get('correo')
        password = serializer.validated_data.get('password')

        try:
            # Obtener usuario con roles y permisos
            #usuario = Usuario.objects.prefetch_related(
             #   Prefetch('usuariorolsucursal_set', queryset=UsuarioRolSucursal.objects.select_related('rol')),
            #).get(correo=correo)
            usuario = Usuario.objects.select_related().prefetch_related(
                Prefetch(
                    'usuariorolsucursal_set',
                    queryset=UsuarioRolSucursal.objects.select_related('rol', 'sucursal')
                )
            ).get(correo=correo)


            # Verificar si el usuario está activo
            if not usuario.estado:
                return Response({'error': 'No puedes iniciar sesión!!!. Comuníquese con el administrador.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Verificar contraseña
            if not check_password(password, usuario.password):
                return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener la primera sucursal asignada
            sucursal = None
            if usuario.usuariorolsucursal_set.exists():
                sucursal_obj = usuario.usuariorolsucursal_set.first().sucursal
                sucursal = {
                    'id': sucursal_obj.id,
                    'nombre': sucursal_obj.nombre,
                    'direccion': sucursal_obj.direccion,
                    'estado': sucursal_obj.estado
                }


            # Generar token JWT
            refresh = RefreshToken.for_user(usuario)
            access_token = str(refresh.access_token)

            # Obtener roles y permisos
            roles = []
            permisos = []

            for usuario_rol in usuario.usuariorolsucursal_set.all():
                rol = usuario_rol.rol
                roles.append(rol.nombre)

                # Obtener permisos para cada rol
                permisos += [rp.permiso.nombre for rp in rol.rolpermiso_set.all()]

            # Verificar si el usuario tiene roles y permisos
            if not roles or not permisos:
                return Response({'error': 'El usuario no tiene roles ni permisos asignados.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Enviar respuesta con token y datos del usuario
            return Response({
                'access_token': access_token,
                'roles': roles,
                'permisos': permisos,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'imagen_url': usuario.imagen_url,
                'usuario_id': usuario.id,
                'sucursal': sucursal  # <- AÑADIDO
            }, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)