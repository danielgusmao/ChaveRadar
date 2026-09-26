from django.contrib import admin
from django.utils import timezone

from .models import UserApproval


@admin.register(UserApproval)
class UserApprovalAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "requested_at", "reviewed_at", "reviewed_by")
    list_filter = ("status", "requested_at", "reviewed_at")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
    readonly_fields = ("requested_at", "reviewed_at", "reviewed_by")
    actions = ("approve_selected", "reject_selected")

    @admin.action(description="Aprovar usuarios selecionados")
    def approve_selected(self, request, queryset):
        for approval in queryset.select_related("user"):
            approval.user.is_active = True
            approval.user.save(update_fields=["is_active"])
            approval.status = UserApproval.STATUS_APPROVED
            approval.reviewed_at = timezone.now()
            approval.reviewed_by = request.user
            approval.save(update_fields=["status", "reviewed_at", "reviewed_by"])

    @admin.action(description="Rejeitar usuarios selecionados")
    def reject_selected(self, request, queryset):
        for approval in queryset.select_related("user"):
            approval.user.is_active = False
            approval.user.save(update_fields=["is_active"])
            approval.status = UserApproval.STATUS_REJECTED
            approval.reviewed_at = timezone.now()
            approval.reviewed_by = request.user
            approval.save(update_fields=["status", "reviewed_at", "reviewed_by"])
