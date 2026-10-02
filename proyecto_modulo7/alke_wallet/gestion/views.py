from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db import connection
from django.db.models import Count, Q, Sum
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
)

from .forms import ClienteForm, CuentaForm, TransaccionEdicionForm, TransaccionForm
from .models import Cliente, Cuenta, Moneda, Transaccion

FORM = "gestion/formulario.html"
CONFIRMAR = "gestion/confirmar_eliminar.html"


class EliminarSeguroMixin:
    """Muestra un mensaje en lugar de un error 500 si el registro no se puede borrar."""

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "No se puede eliminar: tiene registros asociados.")
        except ValidationError as e:
            messages.error(self.request, e.messages[0])
        return redirect(self.success_url)


# --- Inicio y reportes ---------------------------------------------------------
class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "gestion/inicio.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["totales"] = (
            Moneda.objects.annotate(total=Sum("cuentas__saldo"), n_cuentas=Count("cuentas"))
            .filter(n_cuentas__gt=0)
        )
        ctx["n_clientes"] = Cliente.objects.count()
        ctx["n_cuentas"] = Cuenta.objects.filter(activa=True).count()
        ctx["ultimas"] = Transaccion.objects.select_related(
            "cuenta_origen__cliente", "cuenta_destino__cliente"
        )[:5]
        return ctx


class ReportesView(LoginRequiredMixin, TemplateView):
    template_name = "gestion/reportes.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 1) ORM: filter + exclude + annotate
        ctx["cuentas_movimiento"] = (
            Cuenta.objects.filter(activa=True)
            .exclude(enviadas__isnull=True, recibidas__isnull=True)
            .annotate(enviado=Sum("enviadas__monto"), recibido=Sum("recibidas__monto"),
                      n_movimientos=Count("enviadas", distinct=True) + Count("recibidas", distinct=True))
            .select_related("cliente", "moneda")
            .order_by("-n_movimientos")[:5]
        )
        # 2) SQL personalizado con raw() (parametrizado: evita inyección SQL)
        ctx["mayores"] = Transaccion.objects.raw(
            "SELECT id, monto, descripcion, fecha, cuenta_origen_id, cuenta_destino_id "
            "FROM gestion_transaccion WHERE monto >= %s ORDER BY monto DESC LIMIT 5",
            [100],
        )
        # 3) SQL directo con cursor
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT m.codigo, COUNT(c.id), COALESCE(SUM(c.saldo), 0) "
                "FROM gestion_moneda m LEFT JOIN gestion_cuenta c ON c.moneda_id = m.id "
                "GROUP BY m.codigo ORDER BY m.codigo"
            )
            ctx["por_moneda"] = cursor.fetchall()
        return ctx


# --- Clientes -------------------------------------------------------------------
class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "gestion/cliente_list.html"

    def get_queryset(self):
        qs = Cliente.objects.annotate(n_cuentas=Count("cuentas"))
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
        return qs


class ClienteCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = FORM
    success_url = reverse_lazy("gestion:cliente_list")
    success_message = "Cliente creado."
    extra_context = {"titulo": "Nuevo cliente", "boton": "Crear cliente",
                     "volver": reverse_lazy("gestion:cliente_list")}


class ClienteUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = FORM
    success_url = reverse_lazy("gestion:cliente_list")
    success_message = "Cliente actualizado."
    extra_context = {"titulo": "Editar cliente", "boton": "Guardar cambios",
                     "volver": reverse_lazy("gestion:cliente_list")}


class ClienteDelete(LoginRequiredMixin, EliminarSeguroMixin, SuccessMessageMixin, DeleteView):
    model = Cliente
    template_name = CONFIRMAR
    success_url = reverse_lazy("gestion:cliente_list")
    success_message = "Cliente eliminado."
    extra_context = {"volver": reverse_lazy("gestion:cliente_list")}


# --- Cuentas --------------------------------------------------------------------
class CuentaList(LoginRequiredMixin, ListView):
    model = Cuenta
    template_name = "gestion/cuenta_list.html"

    def get_queryset(self):
        return Cuenta.objects.select_related("cliente", "moneda")


class CuentaDetail(LoginRequiredMixin, DetailView):
    model = Cuenta
    template_name = "gestion/cuenta_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["movimientos"] = Transaccion.objects.filter(
            Q(cuenta_origen=self.object) | Q(cuenta_destino=self.object)
        ).select_related("cuenta_origen", "cuenta_destino")
        return ctx


class CuentaCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = FORM
    success_url = reverse_lazy("gestion:cuenta_list")
    success_message = "Cuenta creada."
    extra_context = {"titulo": "Nueva cuenta", "boton": "Crear cuenta",
                     "volver": reverse_lazy("gestion:cuenta_list")}


class CuentaUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = FORM
    success_url = reverse_lazy("gestion:cuenta_list")
    success_message = "Cuenta actualizada."
    extra_context = {"titulo": "Editar cuenta", "boton": "Guardar cambios",
                     "volver": reverse_lazy("gestion:cuenta_list")}


class CuentaDelete(LoginRequiredMixin, EliminarSeguroMixin, SuccessMessageMixin, DeleteView):
    model = Cuenta
    template_name = CONFIRMAR
    success_url = reverse_lazy("gestion:cuenta_list")
    success_message = "Cuenta eliminada."
    extra_context = {"volver": reverse_lazy("gestion:cuenta_list")}


# --- Transacciones --------------------------------------------------------------
class TransaccionList(LoginRequiredMixin, ListView):
    model = Transaccion
    template_name = "gestion/transaccion_list.html"
    paginate_by = 15

    def get_queryset(self):
        return Transaccion.objects.select_related(
            "cuenta_origen__cliente", "cuenta_destino__cliente", "cuenta_origen__moneda"
        )


class TransaccionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = FORM
    success_url = reverse_lazy("gestion:transaccion_list")
    success_message = "Transferencia realizada."
    extra_context = {"titulo": "Nueva transferencia", "boton": "Transferir",
                     "volver": reverse_lazy("gestion:transaccion_list")}


class TransaccionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transaccion
    form_class = TransaccionEdicionForm
    template_name = FORM
    success_url = reverse_lazy("gestion:transaccion_list")
    success_message = "Descripción actualizada."
    extra_context = {"titulo": "Editar descripción", "boton": "Guardar cambios",
                     "volver": reverse_lazy("gestion:transaccion_list")}


class TransaccionDelete(LoginRequiredMixin, EliminarSeguroMixin, SuccessMessageMixin, DeleteView):
    model = Transaccion
    template_name = CONFIRMAR
    success_url = reverse_lazy("gestion:transaccion_list")
    success_message = "Transferencia revertida y eliminada."
    extra_context = {"volver": reverse_lazy("gestion:transaccion_list"),
                     "aviso": "Al eliminarla, los montos vuelven a las cuentas originales."}
