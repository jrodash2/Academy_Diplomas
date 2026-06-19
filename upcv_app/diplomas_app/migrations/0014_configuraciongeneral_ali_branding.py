from django.db import migrations, models


ALI_DEFAULTS = {
    "nombre_institucion": "Academia de Liderazgo, Innovación y Desarrollo Personal",
    "nombre_comercial": "ALI Academy",
    "abreviatura": "ALI",
    "significado_abreviatura": "Academia de Liderazgo e Innovación",
    "descripcion": "Con enfoque en desarrollo personal, tecnología e inteligencia artificial.",
    "slogan": "Formamos personas, impulsamos líderes y conectamos con el futuro.",
}


def seed_ali_configuration(apps, schema_editor):
    ConfiguracionGeneral = apps.get_model("diplomas_app", "ConfiguracionGeneral")
    config = ConfiguracionGeneral.objects.order_by("pk").first()
    if config is None:
        ConfiguracionGeneral.objects.create(pk=1, **ALI_DEFAULTS)
        return
    update_fields = []
    for field, value in ALI_DEFAULTS.items():
        if not getattr(config, field):
            setattr(config, field, value)
            update_fields.append(field)
    legacy_names = {"UPCV", "Unidad para la Prevención Comunitaria de la Violencia"}
    if config.nombre_institucion in legacy_names:
        config.nombre_institucion = ALI_DEFAULTS["nombre_institucion"]
        update_fields.append("nombre_institucion")
    if update_fields:
        config.save(update_fields=list(dict.fromkeys(update_fields)))


class Migration(migrations.Migration):

    dependencies = [
        ("diplomas_app", "0013_configuraciongeneral"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="configuraciongeneral",
            options={"verbose_name": "Configuración institucional", "verbose_name_plural": "Configuración institucional"},
        ),
        migrations.RenameField(
            model_name="configuraciongeneral",
            old_name="logotipo",
            new_name="logo_principal",
        ),
        migrations.RenameField(
            model_name="configuraciongeneral",
            old_name="logotipo2",
            new_name="logo_secundario",
        ),
        migrations.AlterField(
            model_name="configuraciongeneral",
            name="nombre_institucion",
            field=models.CharField(default=ALI_DEFAULTS["nombre_institucion"], max_length=250),
        ),
        migrations.AddField(
            model_name="configuraciongeneral",
            name="nombre_comercial",
            field=models.CharField(blank=True, default=ALI_DEFAULTS["nombre_comercial"], max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="configuraciongeneral",
            name="abreviatura",
            field=models.CharField(blank=True, default=ALI_DEFAULTS["abreviatura"], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="configuraciongeneral",
            name="significado_abreviatura",
            field=models.CharField(blank=True, default=ALI_DEFAULTS["significado_abreviatura"], max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="configuraciongeneral",
            name="descripcion",
            field=models.TextField(blank=True, default=ALI_DEFAULTS["descripcion"], null=True),
        ),
        migrations.AddField(
            model_name="configuraciongeneral",
            name="slogan",
            field=models.CharField(blank=True, default=ALI_DEFAULTS["slogan"], max_length=250, null=True),
        ),
        migrations.RunPython(seed_ali_configuration, migrations.RunPython.noop),
    ]
