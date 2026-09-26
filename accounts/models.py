from django.conf import settings
from django.db import models


class UserApproval(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Aguardando aprovacao"),
        (STATUS_APPROVED, "Aprovado"),
        (STATUS_REJECTED, "Rejeitado"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="approval_request",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_user_approvals",
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at"]
        verbose_name = "Solicitacao de acesso"
        verbose_name_plural = "Solicitacoes de acesso"

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"
