# Generated for ChaveRadar v0.2.3

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserApproval",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("pending", "Aguardando aprovacao"), ("approved", "Aprovado"), ("rejected", "Rejeitado")], default="pending", max_length=20)),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                ("reviewed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reviewed_user_approvals", to=settings.AUTH_USER_MODEL)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="approval_request", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Solicitacao de acesso",
                "verbose_name_plural": "Solicitacoes de acesso",
                "ordering": ["-requested_at"],
            },
        ),
    ]
