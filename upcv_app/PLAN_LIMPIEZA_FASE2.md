# Limpieza de repositorio - Fase 2

## Carpetas eliminadas
- `upcv_app/scompras_app/`: app de compras eliminada por no formar parte del alcance final.
- `upcv_app/tickets_app/`: app de tickets eliminada por no formar parte del alcance final.
- `upcv_app/app_backup/`: respaldo de app eliminado por no ser módulo activo del proyecto final.

## Apps conservadas
El proyecto queda enfocado en:
- Apps internas necesarias de Django: `admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`, `humanize`.
- `empleados_app`: soporte de autenticación, usuarios, grupos/permisos y modelos de empleados/configuración usados por Diplomas.
- `diplomas_app`: módulo funcional principal.

## Rutas finales disponibles
- `/admin/`: administración Django para usuarios, grupos y permisos.
- `/empleados/`: autenticación y soporte mínimo de Empleados.
- `/diplomas/`: módulo Diplomas.
- `/login/` y `/signin/`: alias públicos de inicio de sesión.
- `/logout/`: cierre de sesión.
- `/`: home/login.

## Dependencias revisadas
- No quedan imports activos desde `diplomas_app`, `empleados_app` ni `upcv_app` hacia `scompras_app`, `tickets_app`, `app_backup` o el alias `tickets_db`.
- Se conserva `Empleado` y `ConfiguracionGeneral` porque `diplomas_app` los usa para participantes, datos institucionales, diseño y notificaciones.
- Se conservan las migraciones de `diplomas_app` y `empleados_app`.
- Se conservan los estáticos globales necesarios para las plantillas visuales.

## Advertencias pendientes
- `python manage.py runserver` requiere acceso a PostgreSQL local en `localhost:5432`; en este entorno la conexión fue rechazada.
- La carpeta `upcv_app/backups/` contiene respaldos SQL históricos con referencias a tablas antiguas, pero no forma parte del código Django activo.
