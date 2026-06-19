from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Curso,
    CursoEmpleado,
    DisenoDiploma,
    Firma,
    UbicacionDiploma,
    UsuarioUbicacionDiploma,
)
from .utils import available_manager_users

User = get_user_model()


def normalize_dpi_input(value):
    return "".join(char for char in str(value or "") if char.isdigit())



class ScopedModelFormMixin:
    scope_field_name = "ubicacion"

    def __init__(self, *args, scope=None, **kwargs):
        self.scope = scope or {}
        super().__init__(*args, **kwargs)
        if self.scope_field_name in self.fields:
            if self.scope.get("is_admin"):
                self.fields[self.scope_field_name].queryset = UbicacionDiploma.objects.filter(activa=True).order_by("nombre")
                self.fields[self.scope_field_name].required = True
            else:
                location = self.scope.get("location")
                if location:
                    self.fields[self.scope_field_name].initial = location
                self.fields[self.scope_field_name].widget = forms.HiddenInput()
                self.fields[self.scope_field_name].required = False

    def clean(self):
        cleaned_data = super().clean()
        if self.scope_field_name in self.fields and not self.scope.get("is_admin"):
            location = self.scope.get("location")
            if not location:
                raise forms.ValidationError("Su usuario no tiene una ubicación asignada.")
            cleaned_data[self.scope_field_name] = location
        return cleaned_data


class UbicacionDiplomaForm(forms.ModelForm):
    class Meta:
        model = UbicacionDiploma
        fields = ["nombre", "abreviatura", "descripcion", "activa"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la ubicación"}),
            "abreviatura": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej.: RRHH, FIN, TI"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción opcional"}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_abreviatura(self):
        abreviatura = "".join(char for char in str(self.cleaned_data.get("abreviatura") or "").upper() if char.isalnum())
        if not abreviatura:
            raise forms.ValidationError("Debe ingresar una abreviatura para la ubicación.")
        return abreviatura[:10]


class UsuarioUbicacionDiplomaForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Usuario gestor",
    )
    ubicacion = forms.ModelChoiceField(
        queryset=UbicacionDiploma.objects.filter(activa=True).order_by("nombre"),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Ubicación",
    )

    class Meta:
        model = UsuarioUbicacionDiploma
        fields = ["usuario", "ubicacion"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario"].queryset = available_manager_users()

    def save(self, commit=True, assigned_by=None):
        instance = super().save(commit=False)
        if assigned_by is not None:
            instance.asignado_por = assigned_by
        if commit:
            instance.save()
        return instance


class FirmaForm(ScopedModelFormMixin, forms.ModelForm):
    class Meta:
        model = Firma
        fields = ["ubicacion", "nombre", "rol", "firma"]
        widgets = {
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre completo"}),
            "rol": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej.: Director, Coordinador"}),
            "firma": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class DisenoDiplomaForm(ScopedModelFormMixin, forms.ModelForm):
    class Meta:
        model = DisenoDiploma
        fields = ["ubicacion", "nombre", "descripcion", "imagen_fondo", "activo"]
        widgets = {
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del diseño"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción opcional"}),
            "imagen_fondo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MatriculaManualParticipanteForm(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Curso.objects.none(), widget=forms.HiddenInput(), required=True)

    class Meta:
        model = CursoEmpleado
        fields = [
            "curso",
            "participante_nombre",
            "participante_apellidos",
            "participante_dpi",
            "participante_correo",
            "participante_telefono",
            "participante_institucion",
            "participante_cargo",
            "participante_foto",
            "observaciones",
        ]
        widgets = {
            "participante_nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombres del participante"}),
            "participante_apellidos": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellidos del participante"}),
            "participante_dpi": forms.TextInput(attrs={"class": "form-control", "placeholder": "DPI opcional"}),
            "participante_correo": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
            "participante_telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono opcional"}),
            "participante_institucion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Institución opcional"}),
            "participante_cargo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Cargo opcional"}),
            "participante_foto": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Notas internas u observaciones opcionales"}),
        }
        labels = {
            "participante_nombre": "Nombres *",
            "participante_apellidos": "Apellidos",
            "participante_dpi": "DPI (opcional)",
            "participante_correo": "Correo electrónico (opcional)",
            "participante_telefono": "Teléfono (opcional)",
            "participante_institucion": "Institución (opcional)",
            "participante_cargo": "Cargo (opcional)",
            "participante_foto": "Fotografía (opcional)",
            "observaciones": "Observaciones (opcional)",
        }

    def __init__(self, *args, scope=None, course=None, **kwargs):
        self.scope = scope or {}
        self.course = course
        super().__init__(*args, **kwargs)
        cursos = Curso.objects.all().order_by("nombre")
        if not self.scope.get("is_admin"):
            location = self.scope.get("location")
            cursos = cursos.filter(ubicacion=location) if location else cursos.none()
        self.fields["curso"].queryset = cursos
        if course is not None:
            self.fields["curso"].initial = course
        self.fields["participante_nombre"].required = True
        for field_name in (
            "participante_apellidos",
            "participante_dpi",
            "participante_correo",
            "participante_telefono",
            "participante_institucion",
            "participante_cargo",
            "participante_foto",
            "observaciones",
        ):
            self.fields[field_name].required = False

    def clean_participante_dpi(self):
        return normalize_dpi_input(self.cleaned_data.get("participante_dpi"))

    def clean_participante_nombre(self):
        nombre = " ".join(str(self.cleaned_data.get("participante_nombre") or "").split())
        if not nombre:
            raise forms.ValidationError("Debe ingresar los nombres del participante.")
        return nombre

    def clean_participante_apellidos(self):
        return " ".join(str(self.cleaned_data.get("participante_apellidos") or "").split())

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get("curso") or self.course
        dpi = cleaned_data.get("participante_dpi")
        queryset = CursoEmpleado.objects.filter(curso=curso, participante_dpi=dpi) if curso and dpi else CursoEmpleado.objects.none()
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("Ya existe un participante inscrito en este curso con ese DPI.")
        return cleaned_data


class EditarParticipanteCursoForm(forms.ModelForm):
    class Meta:
        model = CursoEmpleado
        fields = [
            "participante_nombre",
            "participante_apellidos",
            "participante_dpi",
            "participante_correo",
            "participante_telefono",
            "participante_institucion",
            "participante_cargo",
            "participante_foto",
            "observaciones",
        ]
        widgets = MatriculaManualParticipanteForm.Meta.widgets
        labels = MatriculaManualParticipanteForm.Meta.labels

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participante_nombre"].required = True
        for field_name in self.fields:
            if field_name != "participante_nombre":
                self.fields[field_name].required = False

    def clean_participante_dpi(self):
        return normalize_dpi_input(self.cleaned_data.get("participante_dpi"))

    def clean_participante_nombre(self):
        nombre = " ".join(str(self.cleaned_data.get("participante_nombre") or "").split())
        if not nombre:
            raise forms.ValidationError("Debe ingresar los nombres del participante.")
        return nombre

    def clean_participante_apellidos(self):
        return " ".join(str(self.cleaned_data.get("participante_apellidos") or "").split())

    def clean(self):
        cleaned_data = super().clean()
        curso = getattr(self.instance, "curso", None)
        dpi = cleaned_data.get("participante_dpi")
        if curso and dpi:
            duplicate = CursoEmpleado.objects.filter(curso=curso, participante_dpi=dpi).exclude(id=self.instance.id).exists()
            if duplicate:
                raise forms.ValidationError("Ya existe otro participante inscrito en este curso con ese DPI.")
        return cleaned_data


class PublicCourseRegistrationForm(forms.Form):
    codigo_curso = forms.CharField(
        label="Código del curso *",
        max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej.: 12345"}),
        help_text="Ingrese el código real del curso para validar que se registrará al curso correcto.",
    )
    nombre_curso = forms.CharField(
        label="Curso encontrado",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly", "placeholder": "El nombre del curso aparecerá automáticamente"}),
    )
    participante_nombre = forms.CharField(
        label="Nombres *",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombres del participante"}),
    )
    participante_apellidos = forms.CharField(
        label="Apellidos",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellidos del participante"}),
    )
    dpi = forms.CharField(
        label="DPI (opcional)",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "DPI opcional"}),
    )
    participante_correo = forms.EmailField(label="Correo electrónico (opcional)", required=False, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}))
    participante_telefono = forms.CharField(label="Teléfono (opcional)", required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Número telefónico opcional"}))
    participante_institucion = forms.CharField(label="Institución (opcional)", required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Institución"}))
    participante_cargo = forms.CharField(label="Cargo (opcional)", required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Cargo"}))
    participante_foto = forms.ImageField(label="Fotografía (opcional)", required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"}))
    observaciones = forms.CharField(label="Observaciones (opcional)", required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Notas u observaciones opcionales"}))

    def clean_dpi(self):
        return normalize_dpi_input(self.cleaned_data.get("dpi"))

    def clean_codigo_curso(self):
        codigo = "".join(str(self.cleaned_data.get("codigo_curso") or "").split())
        if not codigo:
            raise forms.ValidationError("Debe ingresar el código del curso.")
        return codigo

    def clean_participante_nombre(self):
        nombre = " ".join(str(self.cleaned_data.get("participante_nombre") or "").split())
        if not nombre:
            raise forms.ValidationError("Debe ingresar los nombres del participante.")
        return nombre


class PublicDiplomaDownloadForm(forms.Form):
    codigo_curso = forms.CharField(
        label="Código del curso *",
        max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej.: 12345"}),
        help_text="Ingrese el código del curso exactamente como se lo compartieron.",
    )
    nombre_curso = forms.CharField(
        label="Curso encontrado",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly", "placeholder": "El nombre del curso aparecerá automáticamente"}),
    )
    dpi = forms.CharField(
        label="DPI del participante *",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "DPI registrado en la matrícula"}),
        help_text="Se valida únicamente contra matrículas guardadas en Diplomas.",
    )

    def clean_dpi(self):
        dpi = normalize_dpi_input(self.cleaned_data.get("dpi"))
        if not dpi:
            raise forms.ValidationError("Debe ingresar el DPI registrado en la matrícula.")
        return dpi

    def clean_codigo_curso(self):
        codigo = "".join(str(self.cleaned_data.get("codigo_curso") or "").split())
        if not codigo:
            raise forms.ValidationError("Debe ingresar el código del curso.")
        return codigo


class CursoForm(ScopedModelFormMixin, forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["ubicacion", "codigo", "nombre", "descripcion", "fecha_inicio", "fecha_fin", "firmas", "diseno_diploma"]
        widgets = {
            "ubicacion": forms.Select(attrs={"class": "form-control"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "maxlength": "5", "placeholder": "Ej: 12345"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del curso"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción del curso"}),
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
            "firmas": forms.SelectMultiple(attrs={"class": "form-control", "size": 5}),
            "diseno_diploma": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, scope=None, **kwargs):
        super().__init__(*args, scope=scope, **kwargs)
        self.fields["fecha_inicio"].input_formats = ["%Y-%m-%d"]
        self.fields["fecha_fin"].input_formats = ["%Y-%m-%d"]
        firmas = Firma.objects.all().order_by("nombre")
        disenos = DisenoDiploma.objects.filter(activo=True).order_by("nombre")
        if not (self.scope or {}).get("is_admin"):
            location = (self.scope or {}).get("location")
            firmas = firmas.filter(ubicacion=location) if location else firmas.none()
            disenos = disenos.filter(ubicacion=location) if location else disenos.none()
        self.fields["ubicacion"].empty_label = "Seleccione una ubicación"
        self.fields["ubicacion"].error_messages["required"] = "Debe seleccionar una ubicación."
        self.fields["codigo"].error_messages["required"] = "Debe ingresar el código del curso."
        self.fields["nombre"].error_messages["required"] = "Debe ingresar el nombre del curso."
        self.fields["fecha_inicio"].error_messages["required"] = "Debe ingresar la fecha de inicio."
        self.fields["fecha_fin"].error_messages["required"] = "Debe ingresar la fecha de fin."
        self.fields["firmas"].queryset = firmas
        self.fields["firmas"].required = False
        self.fields["firmas"].label = "Firmas que aparecerán en el diploma"
        self.fields["diseno_diploma"].queryset = disenos
        self.fields["diseno_diploma"].required = False
        self.fields["diseno_diploma"].empty_label = "Seleccione un diseño"
        self.fields["diseno_diploma"].label = "Diseño de diploma"

    def clean_codigo(self):
        codigo = str(self.cleaned_data.get("codigo") or "").strip()
        if not codigo:
            raise forms.ValidationError("Debe ingresar el código del curso.")
        if len(codigo) != 5 or not codigo.isdigit():
            raise forms.ValidationError("El código debe tener 5 dígitos.")
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        ubicacion = cleaned_data.get("ubicacion")
        diseno = cleaned_data.get("diseno_diploma")
        firmas = cleaned_data.get("firmas")

        if ubicacion and diseno and diseno.ubicacion_id != ubicacion.id:
            self.add_error("diseno_diploma", "El diseño seleccionado no pertenece a la ubicación del curso.")

        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error("fecha_fin", "La fecha de fin no puede ser anterior a la fecha de inicio.")

        if ubicacion and firmas:
            firmas_invalidas = [firma.nombre for firma in firmas if firma.ubicacion_id != ubicacion.id]
            if firmas_invalidas:
                self.add_error("firmas", f"Las siguientes firmas no pertenecen a la ubicación seleccionada: {', '.join(firmas_invalidas)}")

        return cleaned_data
