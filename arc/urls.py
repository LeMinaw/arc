from django.contrib import admin
from django.urls import path


admin.site.site_title = "ARC"
admin.site.site_header = "Administration d'ARC"
admin.site.index_title = "Bienvenue dans l'administration d'ARC."

urlpatterns = [
    path("admin/", admin.site.urls),
]
