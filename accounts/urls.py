from django.urls import path

from . import views

urlpatterns = [
    path("entrar/", views.login_view, name="login"),
    path("cadastro/", views.register_view, name="register"),
    path("cadastro/aguardando/", views.registration_pending, name="registration_pending"),
    path("sair/", views.logout_view, name="logout"),
    path("usuarios/pendentes/", views.pending_users, name="pending_users"),
    path("usuarios/pendentes/<int:approval_id>/<str:action>/", views.approval_action, name="approval_action"),
]
