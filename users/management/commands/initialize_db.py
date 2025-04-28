from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import Roles, Permisos, Usuarios, UsuariosRoles, RolesPermisos
from datetime import date

class Command(BaseCommand):
    help = 'Inicializa la base de datos con datos básicos'

    def handle(self, *args, **kwargs):
        self.stdout.write("Inicializando base de datos...")
        
        # 1. Crear Roles
        admin_role, _ = Roles.objects.get_or_create(
            nombre_rol="Administrador",
            defaults={'estado_Rol': True}
        )
        
        # 2. Crear Permisos
        permisos_data = [
            {"nombre_permiso": "registrarUsuarios", "descripcion": "Permite registrar usuarios"},
            {"nombre_permiso": "registrarRoles", "descripcion": "Permite registrar roles"},
            {"nombre_permiso": "registrarPermisos", "descripcion": "a"},
            {"nombre_permiso": "registrarUsuarioRoles", "descripcion": "a"},
            {"nombre_permiso": "registrarRolesPermisos", "descripcion": "a"},
            {"nombre_permiso": "registrarCategorias", "descripcion": "a"},
            {"nombre_permiso": "registrarProductos", "descripcion": "a"},
            {"nombre_permiso": "registrarVenta", "descripcion": "a"},
            {"nombre_permiso": "registrarDetalleVenta", "descripcion": "a"},
            {"nombre_permiso": "registrarVenta-DetalleVenta-Empleado", "descripcion": "a"},
        ]
        
        permisos_objects = []
        for permiso in permisos_data:
            p, _ = Permisos.objects.get_or_create(
                nombre_permiso=permiso["nombre_permiso"],
                defaults={
                    'descripcion': permiso.get("descripcion", ""),
                    'estado_Permiso': True
                }
            )
            permisos_objects.append(p)
        
        # 3. Crear Usuario Admin
        admin_user, created = Usuarios.objects.get_or_create(
            ci="13247291",
            defaults={
                'nombre_usuario': "Andres Benito",
                'apellido': "Yucra",
                'fecha_nacimiento': date(1998, 11, 6),
                'telefono': "72937437",
                'correo': "benitoandrescalle035@gmail.com",
                'password': make_password("Andres1234*"),
                'ci_departamento': "LP",
                'estado_Usuario': True,
                'imagen_url': "http://res.cloudinary.com/dlrpns8z7/image/upload/v1743595809/fnsesmm80hgwelhyzaie.jpg"
            }
        )
        
        if created:
            self.stdout.write(f"Usuario administrador creado: {admin_user}")
        
        # 4. Asignar Rol al Usuario
        UsuariosRoles.objects.get_or_create(
            usuario=admin_user,
            rol=admin_role
        )
        
        # 5. Asignar Permisos al Rol
        for permiso in permisos_objects:
            RolesPermisos.objects.get_or_create(
                rol=admin_role,
                permiso=permiso
            )
        
        self.stdout.write(self.style.SUCCESS("Base de datos inicializada exitosamente!"))

        """ paso 1 """
        """ python manage.py initialize_db """ 
        """ ejecutar el comando en la terminal """
        """ paso 2 """
        """ python manage.py runserver """
        """ ejecutar el servidor para ver los cambios en la base de datos """