from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewsAutenticaion import SucursalViewSet, RolViewSet, PermisoViewSet, UsuarioViewSet, UsuarioRolSucursalViewSet, RolPermisoViewSet
from .viewsProductos import ProductoMaderaViewSet, VentaViewSet, DetalleVentaMaderaViewSet, FacturaReciboViewSet

from . import viewsAutenticaion, viewsProductos

ruter = DefaultRouter()
ruter.register(r'sucursal', SucursalViewSet)
ruter.register(r'rol', RolViewSet)
ruter.register(r'permiso', PermisoViewSet)
ruter.register(r'usuario', UsuarioViewSet)
ruter.register(r'usuariorolsucursal', UsuarioRolSucursalViewSet)
ruter.register(r'rolpermiso', RolPermisoViewSet)

ruter.register(r'productoMadera', ProductoMaderaViewSet)
ruter.register(r'venta', VentaViewSet)
ruter.register(r'detalleventamadera', DetalleVentaMaderaViewSet)
ruter.register(r'facturarecibo', FacturaReciboViewSet)
urlpatterns = [
    path('', include(ruter.urls)),
]