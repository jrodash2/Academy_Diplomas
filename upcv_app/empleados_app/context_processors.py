"""Context processors seguros para el proyecto enfocado en Diplomas.

Las integraciones de compras y tickets fueron retiradas en la Fase 2, por lo que
este módulo no debe importar apps eliminadas ni exponer permisos de esos módulos.
"""


def frase_del_dia(request):
    return {"frase_del_dia": None}


def grupo_usuario(request):
    if not request.user.is_authenticated:
        return {}

    return {
        "es_administrador": request.user.groups.filter(name="Administrador").exists(),
    }


def datos_institucion(request):
    return {"institucion": None}


def empleado_context(request):
    return {"empleado": None, "empleado_foto_url": None}
