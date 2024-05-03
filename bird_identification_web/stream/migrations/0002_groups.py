from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    viewers_group = Group.objects.get_or_create(name="stream_viewers")[0]
    
    Permission = apps.get_model('auth', 'Permission')
    permissions = Permission.objects.filter(content_type__app_label='stream')

    viewers_group.permissions.add(permissions.filter(codename='view_stream')[0])

class Migration(migrations.Migration):
    dependencies = [('stream', '0001_permissions')]

    operations = [
        migrations.RunPython(create_groups),
    ]
