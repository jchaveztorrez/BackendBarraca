# BackendBarraca
<h1 align="center">T i e n d a - O n l i n e</h1>

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg" alt="Angular Logo" width="100"/>
  <img src="https://www.opengis.ch/wp-content/uploads/2020/04/django-python-logo.png" alt="Django Logo" width="100"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" alt="PostgreSQL Logo" width="100"/>
</p>



<table>
  <tr>
    <td><h1>Framework Django</h1></td>
    <td><img src="https://www.opengis.ch/wp-content/uploads/2020/04/django-python-logo.png" alt="Django Logo" width="100"/></td>
  </tr>
</table>


## Instalaciones

Para comenzar a usar este proyecto, necesitarás instalar las siguientes dependencias:

```bash
# Instalar virtualenv, que te permitirá crear un entorno aislado
pip install virtualenv

# Crear un entorno virtual
virtualenv venv

# O para activar en Windows
env\Scripts\activate
./venv/Scripts/activate   

# Instalar Django, el framework principal para el backend
pip install django

# Crear un nuevo proyecto Django
django-admin startproject tienda_online

```
## Otras dependencias importantes
Aquí se listan más paquetes que puedes necesitar para tu proyecto Django:
```bash
# Instalar Django REST Framework, necesario si planeas crear APIs
pip install djangorestframework
pip install djangorestframework-simplejwt

# Instalar django-cors-headers, útil para manejar las solicitudes entre el frontend (Angular) y el backend (Django)
pip install django-cors-headers

# Instalar psycopg2, necesario para conectarse a bases de datos PostgreSQL
pip install psycopg2

```

## Creación de archivos
```bash
# Crear un nuevo proyecto Django llamado 'main'
django-admin startproject main .

# Crear una nueva aplicación dentro del proyecto llamada 'users'
django-admin startapp users

```
## Migraciones
Las migraciones en Django permiten que los cambios en los modelos de la base de datos se reflejen de manera automática. Aquí están los comandos para hacer migraciones y aplicar los cambios:
```bash
# Crear migraciones para la app 'users'
python manage.py makemigrations users

# Aplicar las migraciones
python manage.py migrate

# Crear un superusuario para acceder al panel de administración de Django
python manage.py createsuperuser

# Iniciar el servidor local para probar la aplicación
python manage.py runserver

```
