
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewsAutenticaion import  CategoriasViewSet, DetallesVentasViewSet, FacturaReciboViewSet, LoginView, ProductoMaderaViewSet, SucursalViewSet, RolViewSet, PermisoViewSet, UsuarioViewSet, UsuarioRolSucursalViewSet, RolPermisoViewSet, VentasViewSet


from . import viewsAutenticaion

ruter = DefaultRouter()
ruter.register(r'sucursal', SucursalViewSet)
ruter.register(r'rol', RolViewSet)
ruter.register(r'permiso', PermisoViewSet)
ruter.register(r'usuario', UsuarioViewSet)
ruter.register(r'usuariorolsucursal', UsuarioRolSucursalViewSet)
ruter.register(r'rolpermiso', RolPermisoViewSet)

ruter.register(r'categorias', CategoriasViewSet)  
ruter.register(r'productoMadera', ProductoMaderaViewSet)
ruter.register(r'venta', VentasViewSet)
ruter.register(r'detalleventamadera', DetallesVentasViewSet)
ruter.register(r'facturarecibo', FacturaReciboViewSet)
#         fields = '__all__'

urlpatterns = [
    path('', include(ruter.urls)),
    path('login/', LoginView.as_view(), name='login'),
]