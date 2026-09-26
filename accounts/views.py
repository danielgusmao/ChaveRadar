from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm
from .models import UserApproval


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect("dashboard")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        request.session["pending_registration_email"] = user.email
        return redirect("registration_pending")

    return render(request, "accounts/register.html", {"form": form})


def registration_pending(request):
    email = request.session.pop("pending_registration_email", "")
    return render(request, "accounts/registration_pending.html", {"email": email})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


@staff_member_required(login_url="login")
def pending_users(request):
    pending = (
        UserApproval.objects.filter(status=UserApproval.STATUS_PENDING)
        .select_related("user")
        .order_by("requested_at")
    )
    approved_count = UserApproval.objects.filter(status=UserApproval.STATUS_APPROVED).count()
    rejected_count = UserApproval.objects.filter(status=UserApproval.STATUS_REJECTED).count()
    return render(
        request,
        "accounts/pending_users.html",
        {
            "pending_users": pending,
            "pending_count": pending.count(),
            "approved_count": approved_count,
            "rejected_count": rejected_count,
        },
    )


@staff_member_required(login_url="login")
@require_POST
def approval_action(request, approval_id, action):
    approval = get_object_or_404(UserApproval.objects.select_related("user"), pk=approval_id)
    user = approval.user

    if action == "approve":
        user.is_active = True
        user.save(update_fields=["is_active"])
        approval.status = UserApproval.STATUS_APPROVED
        approval.reviewed_at = timezone.now()
        approval.reviewed_by = request.user
        approval.save(update_fields=["status", "reviewed_at", "reviewed_by"])
        messages.success(request, f"Acesso de {user.username} aprovado.")
    elif action == "reject":
        user.is_active = False
        user.save(update_fields=["is_active"])
        approval.status = UserApproval.STATUS_REJECTED
        approval.reviewed_at = timezone.now()
        approval.reviewed_by = request.user
        approval.save(update_fields=["status", "reviewed_at", "reviewed_by"])
        messages.info(request, f"Cadastro de {user.username} rejeitado.")
    else:
        messages.error(request, "Acao de aprovacao invalida.")

    return redirect(reverse("pending_users"))
