# Plan de limpieza segura - Fase 1

## Objetivo funcional
Conservar el proyecto funcionando con `diplomas_app` como módulo principal y `empleados_app` como soporte de autenticación, usuarios, grupos, roles/permisos y datos mínimos reutilizados por Diplomas.

## Apps detectadas
- `diplomas_app`: módulo funcional principal de diplomas, cursos, participantes, firmas, diseños, ubicaciones y asignaciones.
- `empleados_app`: módulo de autenticación y soporte de usuarios/perfiles. También contiene modelos institucionales compartidos por Diplomas.
- `scompras_app`: módulo de compras/inventario, actualmente fuera de `INSTALLED_APPS` y sin rutas principales activas.
- `tickets_app`: módulo de tickets, actualmente fuera de `INSTALLED_APPS` y sin rutas principales activas.
- `app_backup`: carpeta de respaldo, no debe considerarse módulo activo.

## Apps que deben quedarse
- `diplomas_app`.
- `empleados_app`.
- Apps core de Django configuradas en `INSTALLED_APPS`: `admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`, `humanize`.

## Apps candidatas para eliminar en Fase 2
No eliminar todavía. Validar respaldos, migraciones, datos y referencias antes de borrar:
- `scompras_app`.
- `tickets_app`.
- `app_backup`.
- Recursos estáticos o templates duplicados generados por esos módulos, si no son usados por Diplomas/Empleados.

## Dependencias de Diplomas que no deben borrarse
`diplomas_app` depende directamente de:
- `empleados_app.models.Empleado` para participantes/empleados asociados a cursos.
- `empleados_app.models.ConfiguracionGeneral` para datos institucionales y notificaciones.
- Autenticación, grupos y permisos de Django (`django.contrib.auth`).
- Archivos estáticos compartidos bajo `static/assets` y `staticfiles/assets` usados por las plantillas base.
- Archivos de media referenciados por diseños, firmas, logos, imágenes institucionales y diplomas generados.

## Dependencias de Empleados que no deben borrarse
`empleados_app` conserva:
- Vistas de login, logout y dashboard mínimo.
- Modelos `Empleado`, `ConfiguracionGeneral`, datos básicos y formación porque son usados por Diplomas o por integraciones existentes.
- Rutas mínimas de perfil/configuración/búsqueda por DPI por compatibilidad.
- Integración con grupos de Django para mantener la lógica actual de acceso.

## Rutas principales seguras actuales
- `/` -> login/home de empleados.
- `/login/` y `/signin/` -> login.
- `/logout/` -> logout.
- `/empleados/` -> rutas mínimas de autenticación/soporte.
- `/diplomas/` -> módulo Diplomas.
- `/admin/` -> administración Django de usuarios, grupos y permisos.

## Rutas que quedarían rotas si se borran módulos sin revisar
- Cualquier enlace histórico a `/scompras/` o `/tickets/` quedaría fuera de servicio; actualmente no están incluidos en el `urls.py` principal.
- Imports directos desde `scompras_app` o `tickets_app` en código activo deben eliminarse o aislarse antes de borrar carpetas.
- Referencias a assets compartidos deben validarse antes de borrar `static`, `staticfiles` o `media`.

## Plan Fase 2 recomendado
1. Ejecutar búsqueda final de referencias a `scompras_app`, `tickets_app`, `scompras` y `tickets`.
2. Confirmar que no existen context processors, routers, imports o templates activos que dependan de esos módulos.
3. Respaldar base de datos y media.
4. Retirar rutas residuales si existieran.
5. Retirar apps no instaladas por módulos completos en una rama separada.
6. Ejecutar `python manage.py check` y pruebas manuales de login, dashboard y flujo de diplomas.
