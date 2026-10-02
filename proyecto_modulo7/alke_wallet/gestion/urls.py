from django.urls import path

from . import views

app_name = "gestion"

urlpatterns = [
    path("", views.InicioView.as_view(), name="inicio"),
    path("reportes/", views.ReportesView.as_view(), name="reportes"),

    path("clientes/", views.ClienteList.as_view(), name="cliente_list"),
    path("clientes/nuevo/", views.ClienteCreate.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/editar/", views.ClienteUpdate.as_view(), name="cliente_update"),
    path("clientes/<int:pk>/eliminar/", views.ClienteDelete.as_view(), name="cliente_delete"),

    path("cuentas/", views.CuentaList.as_view(), name="cuenta_list"),
    path("cuentas/nueva/", views.CuentaCreate.as_view(), name="cuenta_create"),
    path("cuentas/<int:pk>/", views.CuentaDetail.as_view(), name="cuenta_detail"),
    path("cuentas/<int:pk>/editar/", views.CuentaUpdate.as_view(), name="cuenta_update"),
    path("cuentas/<int:pk>/eliminar/", views.CuentaDelete.as_view(), name="cuenta_delete"),

    path("transacciones/", views.TransaccionList.as_view(), name="transaccion_list"),
    path("transacciones/nueva/", views.TransaccionCreate.as_view(), name="transaccion_create"),
    path("transacciones/<int:pk>/editar/", views.TransaccionUpdate.as_view(), name="transaccion_update"),
    path("transacciones/<int:pk>/eliminar/", views.TransaccionDelete.as_view(), name="transaccion_delete"),
]
