from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=150, unique=True)),
                ('display_name', models.CharField(blank=True, max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('alerts_enabled', models.BooleanField(default=True)),
                ('keywords', models.TextField(blank=True, help_text='Palavras adicionais deste perfil, separadas por virgula. Em branco usa a lista global.')),
                ('notes', models.TextField(blank=True)),
                ('last_checked_at', models.DateTimeField(blank=True, null=True)),
                ('last_status', models.CharField(choices=[('waiting', 'Aguardando conexao'), ('ok', 'Monitorado'), ('error', 'Erro')], default='waiting', max_length=20)),
                ('last_error', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instagram_monitoring_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil monitorado do Instagram',
                'verbose_name_plural': 'Perfis monitorados do Instagram',
                'ordering': ['handle'],
            },
        ),
    ]
