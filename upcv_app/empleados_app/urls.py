from django.urls import path
from . import views

app_name = 'empleados'

urlpatterns = [
    # Autenticación y navegación base
    path('login/', views.signin, name='login'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('dahsboard/', views.dahsboard, name='dahsboard'),
    path('', views.home, name='home'),
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:pk>/editar/', views.usuario_editar, name='usuario_editar'),

    # Configuración institucional mínima usada por Diplomas
    path('config_general/', views.configuracion_general, name='configuracion_general'),

    # Perfil básico conservado por compatibilidad con datos de participantes/empleados
    path('empleado/perfil/<int:empleado_id>/', views.perfil_empleado, name='perfil_empleado'),
    path('empleado/<int:empleado_id>/guardar-datos-basicos/', views.guardar_datos_basicos, name='guardar_datos_basicos'),
    path('empleado/<int:empleado_id>/guardar-formacion/', views.guardar_formacion, name='guardar_formacion'),
    path('formacion/<int:formacion_id>/actualizar/', views.actualizar_formacion, name='actualizar_formacion'),
    path('formacion/<int:formacion_id>/eliminar/', views.eliminar_formacion, name='eliminar_formacion'),

    # Búsqueda de empleado por DPI requerida por integraciones existentes
    path('buscar-empleado/', views.buscar_empleado_dpi, name='buscar_empleado_dpi'),
]
