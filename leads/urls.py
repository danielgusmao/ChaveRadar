from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('leads/', views.leads_list, name='leads'),
    path('perfis/', views.profiles_list, name='profiles'),
    path('importar/', views.import_comments, name='import_comments'),
    path('revisao/', views.review_list, name='review'),
    path('revisao/<int:classification_id>/<str:action>/', views.review_action, name='review_action'),
    path('exportar/', views.export_excel, name='export_excel'),
]
