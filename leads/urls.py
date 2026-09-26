from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('leads/', views.leads_list, name='leads'),
    path('perfis/', views.profiles_list, name='profiles'),
    path('perfis/<int:profile_id>/editar/', views.profile_edit, name='profile_edit'),
    path('perfis/<int:profile_id>/excluir/', views.profile_delete, name='profile_delete'),
    path('monitoramento/', views.monitoring_list, name='monitoring'),
    path('monitoramento/<int:profile_id>/editar/', views.monitoring_edit, name='monitoring_edit'),
    path('monitoramento/<int:profile_id>/excluir/', views.monitoring_delete, name='monitoring_delete'),
    path('importar/', views.import_comments, name='import_comments'),
    path('revisao/', views.review_list, name='review'),
    path('revisao/<int:classification_id>/<str:action>/', views.review_action, name='review_action'),
    path('revisao/aprovar-selecionados/', views.review_bulk_approve, name='review_bulk_approve'),
    path('exportar/', views.export_excel, name='export_excel'),
]
