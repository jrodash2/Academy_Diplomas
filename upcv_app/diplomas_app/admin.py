from django.contrib import admin

from .models import ConfiguracionGeneral, Curso, CursoEmpleado, Diploma, DisenoDiploma, Firma, FraseMotivacional, UbicacionDiploma


@admin.register(ConfiguracionGeneral)
class ConfiguracionGeneralAdmin(admin.ModelAdmin):
    list_display = ("nombre_institucion", "correo", "telefono", "actualizado")
    search_fields = ("nombre_institucion", "correo", "telefono")

    def has_add_permission(self, request):
        if ConfiguracionGeneral.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(FraseMotivacional)
class FraseMotivacionalAdmin(admin.ModelAdmin):
    list_display = ("personaje", "frase")
    search_fields = ("personaje", "frase")


@admin.register(UbicacionDiploma)
class UbicacionDiplomaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "abreviatura", "activa", "creado_en")
    search_fields = ("nombre", "abreviatura")
    list_filter = ("activa", "creado_en")


@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rol", "ubicacion", "creado_en")
    search_fields = ("nombre", "rol", "ubicacion__nombre", "ubicacion__abreviatura")
    list_filter = ("ubicacion", "creado_en")


@admin.register(DisenoDiploma)
class DisenoDiplomaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "activo", "creado_en", "actualizado_en")
    search_fields = ("nombre", "descripcion", "ubicacion__nombre", "ubicacion__abreviatura")
    list_filter = ("ubicacion", "activo", "creado_en")


class CursoEmpleadoInline(admin.TabularInline):
    model = CursoEmpleado
    extra = 0


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "ubicacion", "diseno_diploma", "fecha_inicio", "fecha_fin", "creado_en")
    search_fields = ("codigo", "nombre", "ubicacion__nombre", "ubicacion__abreviatura")
    list_filter = ("ubicacion", "fecha_inicio", "fecha_fin")
    filter_horizontal = ("firmas",)
    inlines = [CursoEmpleadoInline]
    readonly_fields = ("posiciones",)


@admin.register(CursoEmpleado)
class CursoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre_participante", "participante_dpi", "curso", "participante_correo", "fecha_asignacion")
    search_fields = ("participante_nombre", "participante_apellidos", "participante_dpi", "participante_correo", "curso__nombre", "curso__ubicacion__abreviatura")
    list_filter = ("curso__ubicacion", "curso", "fecha_asignacion")
    autocomplete_fields = ("curso",)


@admin.register(Diploma)
class DiplomaAdmin(admin.ModelAdmin):
    list_display = ("numero_diploma", "curso_empleado", "fecha_emision", "generado_en")
    search_fields = ("numero_diploma", "curso_empleado__participante_nombre", "curso_empleado__participante_apellidos", "curso_empleado__participante_dpi")
    list_filter = ("fecha_emision", "generado_en")
    autocomplete_fields = ("curso_empleado",)
    readonly_fields = ("generado_en",)
