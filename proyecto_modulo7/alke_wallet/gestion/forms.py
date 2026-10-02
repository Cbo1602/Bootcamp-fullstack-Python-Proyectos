from django import forms

from .models import Cliente, Cuenta, Transaccion


class EstiloBootstrapMixin:
    """Agrega las clases de Bootstrap a todos los widgets del formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            w = campo.widget
            if isinstance(w, forms.CheckboxInput):
                clase = "form-check-input"
            elif isinstance(w, forms.Select):  # incluye SelectMultiple
                clase = "form-select"
            else:
                clase = "form-control"
            w.attrs["class"] = clase


class ClienteForm(EstiloBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono", "usuario"]


class CuentaForm(EstiloBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ["cliente", "moneda", "saldo", "co_titulares", "activa"]
        help_texts = {"saldo": "Saldo inicial. Después solo cambia con transacciones."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["saldo"].disabled = True


class TransaccionForm(EstiloBootstrapMixin, forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["cuenta_origen", "cuenta_destino", "monto", "descripcion"]


class TransaccionEdicionForm(EstiloBootstrapMixin, forms.ModelForm):
    """Una transacción ya registrada solo permite corregir su descripción."""

    class Meta:
        model = Transaccion
        fields = ["descripcion"]
