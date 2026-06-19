from django import forms
from .models import Contrato, Empleado, Puesto, Sede
from django.forms import CheckboxInput, DateInput
from .models import ConfiguracionGeneral
from django.contrib.auth.models import User, Group

from django import forms
from .models import DatosBasicosEmpleado, FormacionAcademicaEmpleado

class DatosBasicosEmpleadoForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )

    class Meta:
        model = DatosBasicosEmpleado
        fields = [
            'fecha_nacimiento',
            'sexo',
            'estado_civil',
            'nacionalidad',
            'grupo_etnico',
            'idiomas',
            'direccion_residencia',
            'telefono_personal',
            'telefono_emergencia',
            'persona_contacto_emergencia',
            'correo_institucional',
        ]

        widgets = {
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),

            'grupo_etnico': forms.Select(attrs={
                'class': 'form-control chosen-select'
            }),

            'idiomas': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_residencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_personal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_emergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'persona_contacto_emergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Forzar formato correcto en edición
        if self.instance and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')


class FormacionAcademicaEmpleadoForm(forms.ModelForm):
    class Meta:
        model = FormacionAcademicaEmpleado
        fields = [
            'nivel',
            'titulo_obtenido',
            'centro_estudio',
            'fecha',
        ]

        widgets = {
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'titulo_obtenido': forms.TextInput(attrs={'class': 'form-control'}),
            'centro_estudio': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
        }

    # Importante: permitir inicializar correctamente el valor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fecha:
            self.fields['fecha'].initial = self.instance.fecha.strftime('%Y-%m-%d')


class ConfiguracionGeneralForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGeneral
        fields = ['nombre_institucion', 'direccion', 'logotipo', 'logotipo2']
        
    # Personalizamos la clase 'form-control' para otros campos si es necesario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadimos 'form-control' a los campos, si no está especificado en los widgets
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'



class UserForm(forms.ModelForm):

    # === Campo adicional DPI ===
    dpi = forms.CharField(
        max_length=20,
        required=True,
        label="DPI del empleado",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese DPI'})
    )

    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar Contraseña"
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Grupo"
    )

    class Meta:
        model = User
        fields = ['dpi', 'username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("new_password")
        user.set_password(password)

        if commit:
            user.save()
            group = self.cleaned_data.get("group")
            if group:
                user.groups.set([group])

        return user

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombres', 'apellidos', 'dpi', 'imagen', 'tipoc', 'dcargo',  'dcargo2']

    
    # Personalizar los campos para agregar la clase 'form-control'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Agregar la clase 'form-control' a todos los campos del formulario
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'


class EmpleadoeditForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombres', 'apellidos', 'imagen', 'dpi', 'tipoc', 'dcargo',  'dcargo2', 'activo']
        labels = {'activo': 'Activo'}
        widgets = {
            'activo': CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadir la clase 'form-control' a los campos si no está especificado en los widgets
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'fecha_inicio',
            'fecha_vencimiento',
            'tipo_contrato',
            'renglon',
            'sede',
            'puesto',
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-control'}),
            'renglon': forms.Select(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):  # No tocar checkboxes
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
                
        # Desactivar el select de puesto si no hay sede seleccionada
        self.fields['puesto'].widget.attrs['disabled'] = 'disabled'        
                

class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = ['nombre', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PuestoForm(forms.ModelForm):
    class Meta:
        model = Puesto
        fields = ['nombre', 'descripcion', 'sede']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
        }                


class UsuarioSistemaForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    group = forms.ModelChoiceField(
        label="Grupo o rol",
        queryset=Group.objects.all().order_by("name"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Seleccione un grupo",
    )
    is_active = forms.BooleanField(
        label="Usuario activo",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo",
        }

    def __init__(self, *args, **kwargs):
        self.editing = kwargs.pop("editing", False)
        super().__init__(*args, **kwargs)
        if self.editing:
            self.fields["password"].required = False
            self.fields["password_confirm"].required = False
            self.fields["password"].help_text = "Deje en blanco para conservar la contraseña actual."
            if self.instance and self.instance.pk and self.instance.groups.exists():
                self.fields["group"].initial = self.instance.groups.first()

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        qs = User.objects.filter(username__iexact=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre de usuario.")
        return username

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if email:
            qs = User.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe un usuario con ese correo.")
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm = cleaned.get("password_confirm")
        if not self.editing and not password:
            self.add_error("password", "Debe ingresar una contraseña.")
        if password or confirm:
            if password != confirm:
                self.add_error("password_confirm", "Las contraseñas no coinciden.")
        if not cleaned.get("group"):
            self.add_error("group", "Debe seleccionar un grupo.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
            group = self.cleaned_data.get("group")
            user.groups.set([group] if group else [])
        return user
