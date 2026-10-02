from django.contrib import admin

from .models import Cliente, Cuenta, Moneda, Transaccion


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "simbolo")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono", "usuario")
    search_fields = ("nombre", "email")


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("numero", "cliente", "moneda", "saldo", "activa")
    list_filter = ("moneda", "activa")
    search_fields = ("numero", "cliente__nombre")
    filter_horizontal = ("co_titulares",)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("fecha", "cuenta_origen", "cuenta_destino", "monto")
    list_filter = ("fecha",)
    date_hierarchy = "fecha"
