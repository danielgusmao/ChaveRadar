from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import UserApproval


class RegistrationApprovalTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_registration_creates_inactive_pending_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Teste",
                "last_name": "Usuario",
                "email": "teste@example.com",
                "username": "teste.usuario",
                "password1": "SenhaForte!2026",
                "password2": "SenhaForte!2026",
            },
        )
        self.assertRedirects(response, reverse("registration_pending"))
        user = self.User.objects.get(username="teste.usuario")
        self.assertFalse(user.is_active)
        self.assertEqual(user.approval_request.status, UserApproval.STATUS_PENDING)

    def test_anonymous_dashboard_redirects_to_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_staff_can_approve_user(self):
        admin = self.User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="SenhaAdmin!2026",
        )
        user = self.User.objects.create_user(
            username="pendente",
            email="pendente@example.com",
            password="SenhaForte!2026",
            is_active=False,
        )
        approval = UserApproval.objects.create(user=user)
        self.client.force_login(admin)
        response = self.client.post(reverse("approval_action", args=[approval.id, "approve"]))
        self.assertRedirects(response, reverse("pending_users"))
        user.refresh_from_db()
        approval.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(approval.status, UserApproval.STATUS_APPROVED)
        self.assertEqual(approval.reviewed_by, admin)
