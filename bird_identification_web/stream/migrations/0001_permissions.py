from django.db import migrations, models

def create_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')

    view_content_type = ContentType.objects.get_or_create(app_label='stream', model='unused')[0]
    Permission.objects.get_or_create(name='Can view video stream', content_type=view_content_type, codename='view_stream')


class Migration(migrations.Migration):
    dependencies = [('auth', '0001_initial')]

    operations = [
        migrations.RunPython(create_permissions),
    ]
