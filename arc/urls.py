from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


admin.site.site_title = "ARC"
admin.site.site_header = "Administration d'ARC"
admin.site.index_title = "Bienvenue dans l'administration d'ARC."

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include("catalog.urls")),
    path("api/v1/", include("inventory.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
