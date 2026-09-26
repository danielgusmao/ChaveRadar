# Generated for ChaveRadar v0.2.0
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=150, unique=True)),
                ('display_name', models.CharField(blank=True, max_length=255)),
                ('source_type', models.CharField(choices=[('official_api', 'API oficial'), ('manual', 'Importacao manual'), ('provider', 'Provedor licenciado')], default='manual', max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('last_sync_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_media_id', models.CharField(blank=True, max_length=255)),
                ('permalink', models.URLField(max_length=1000)),
                ('media_type', models.CharField(blank=True, max_length=30)),
                ('caption_original', models.TextField(blank=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('property_type', models.CharField(blank=True, max_length=150)),
                ('property_region', models.CharField(blank=True, max_length=255)),
                ('transaction_type', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='leads.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_comment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(max_length=150)),
                ('display_name', models.CharField(blank=True, max_length=255)),
                ('text_original', models.TextField()),
                ('displayed_date_original', models.CharField(blank=True, max_length=100)),
                ('commented_at', models.DateTimeField(blank=True, null=True)),
                ('captured_at', models.DateTimeField(auto_now_add=True)),
                ('source_type', models.CharField(choices=[('official_api', 'API oficial'), ('manual', 'Importacao manual'), ('provider', 'Provedor licenciado')], default='manual', max_length=20)),
                ('raw_payload', models.JSONField(blank=True, default=dict)),
                ('fingerprint', models.CharField(max_length=64, unique=True)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='leads.publication')),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_lead', models.BooleanField(default=False)),
                ('intents', models.JSONField(default=list)),
                ('qualification', models.CharField(choices=[('high', 'Alto'), ('medium', 'Medio'), ('low', 'Baixo'), ('not_lead', 'Nao Lead')], default='not_lead', max_length=20)),
                ('evidence', models.JSONField(default=list)),
                ('confidence', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('exclusion_reason', models.CharField(blank=True, max_length=255)),
                ('review_status', models.CharField(choices=[('auto', 'Auto-aprovado'), ('pending', 'Pendente'), ('approved', 'Aprovado manualmente'), ('rejected', 'Rejeitado manualmente')], default='pending', max_length=20)),
                ('classifier_version', models.CharField(default='0.2.0', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='classification', to='leads.comment')),
            ],
        ),
        migrations.CreateModel(
            name='CollectionRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('publications_found', models.PositiveIntegerField(default=0)),
                ('comments_found', models.PositiveIntegerField(default=0)),
                ('comments_new', models.PositiveIntegerField(default=0)),
                ('comments_duplicate', models.PositiveIntegerField(default=0)),
                ('comments_failed', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(default='running', max_length=30)),
                ('error_message', models.TextField(blank=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_runs', to='leads.profile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='publication',
            constraint=models.UniqueConstraint(fields=('profile', 'permalink'), name='uq_profile_publication'),
        ),
    ]
