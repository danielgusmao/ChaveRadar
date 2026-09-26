from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ChaveRadar - Administracao"
admin.site.site_title = "ChaveRadar"
admin.site.index_title = "Painel administrativo"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("leads.urls")),
]
