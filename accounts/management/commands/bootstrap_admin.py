import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserApproval


class Command(BaseCommand):
    help = "Cria o primeiro administrador usando variaveis de ambiente, sem sobrescrever senha existente."

    def handle(self, *args, **options):
        username = os.environ.get("CHAVERADAR_ADMIN_USERNAME", "").strip()
        email = os.environ.get("CHAVERADAR_ADMIN_EMAIL", "").strip().lower()
        password = os.environ.get("CHAVERADAR_ADMIN_PASSWORD", "")

        if not username or not email or not password:
            self.stdout.write("bootstrap_admin: variaveis nao definidas; nenhuma alteracao realizada.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        changed_fields = []
        if created:
            user.set_password(password)
            changed_fields.append("password")
        if user.email != email:
            user.email = email
            changed_fields.append("email")
        if not user.is_active:
            user.is_active = True
            changed_fields.append("is_active")
        if not user.is_staff:
            user.is_staff = True
            changed_fields.append("is_staff")
        if not user.is_superuser:
            user.is_superuser = True
            changed_fields.append("is_superuser")

        if changed_fields:
            user.save()

        UserApproval.objects.update_or_create(
            user=user,
            defaults={"status": UserApproval.STATUS_APPROVED},
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Administrador '{username}' criado com sucesso."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Administrador '{username}' ja existe; permissoes confirmadas."))
