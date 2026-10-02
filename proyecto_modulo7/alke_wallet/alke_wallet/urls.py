from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Alke Wallet - Administración"
admin.site.site_title = "Alke Wallet"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login / logout
    path("", include("gestion.urls")),
]
