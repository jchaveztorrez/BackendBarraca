from django.shortcuts import render
from .models import ProductoMadera, Sucursal, Venta, DetalleVentaMadera, FacturaRecibo
from .serializers import ProductoMaderaSerializer, VentaSerializer, DetalleVentaMaderaSerializer, FacturaReciboSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class ProductoMaderaViewSet(viewsets.ModelViewSet):
    queryset = ProductoMadera.objects.all()
    serializer_class = ProductoMaderaSerializer

    def create(self, request, *args, **kwargs):
        # Extraer datos del request
        data = {key: request.data.get(key) for key in [
            'especie', 'ancho', 'espesor', 'largo', 'cantidad', 
            'precio_compra', 'precio_barraca', 'precio_venta'
        ]}

        # Obtener la sucursal como instancia de Sucursal
        sucursal_id = request.data.get('sucursal')
        try:
            data['sucursal'] = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            return Response({"error": "La sucursal especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el producto ya existe con esas características (especie, dimensiones y sucursal)
        if ProductoMadera.objects.filter(
            especie=data['especie'],
            ancho=data['ancho'],
            espesor=data['espesor'],
            largo=data['largo'],
            sucursal=data['sucursal']
        ).exists():
            return Response(
                {'detail': 'Ya existe un producto con esa especie, dimensiones y sucursal.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el producto de madera
        producto_madera = ProductoMadera.objects.create(**data)

        # Serializar el producto recién creado
        return Response(ProductoMaderaSerializer(producto_madera).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        # Actualizar sucursal si se proporciona
        sucursal_id = data.get('sucursal')
        if sucursal_id:
            try:
                instance.sucursal = Sucursal.objects.get(id=sucursal_id)
            except Sucursal.DoesNotExist:
                return Response(
                    {"error": "La sucursal especificada no existe."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Actualizar campos básicos
        for field in [
            'especie', 'ancho', 'espesor', 'largo',
            'cantidad', 'precio_compra', 'precio_barraca', 'precio_venta'
        ]:
            if field in data:
                setattr(instance, field, data[field])

        # Validar duplicidad de producto con misma especie, dimensiones y sucursal
        if ProductoMadera.objects.exclude(pk=instance.pk).filter(
            especie=instance.especie,
            ancho=instance.ancho,
            espesor=instance.espesor,
            largo=instance.largo,
            sucursal=instance.sucursal
        ).exists():
            return Response(
                {'detail': 'Ya existe otro producto con esa especie, dimensiones y sucursal.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar y guardar cambios
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class DetalleVentaMaderaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVentaMadera.objects.all()
    serializer_class = DetalleVentaMaderaSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class FacturaReciboViewSet(viewsets.ModelViewSet):
    queryset = FacturaRecibo.objects.all()
    serializer_class = FacturaReciboSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)