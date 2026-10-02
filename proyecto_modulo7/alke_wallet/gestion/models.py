import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models, transaction
from django.db.models import F


class Moneda(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=50)
    simbolo = models.CharField(max_length=3)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} ({self.simbolo})"


class Cliente(models.Model):
    # Uno a Uno: un cliente puede estar vinculado a un usuario de django.contrib.auth
    usuario = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="cliente"
    )
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^\+?\d{7,15}$", "Ingresa solo números (7 a 15 dígitos), con + opcional.")],
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    # Muchos a Uno: un cliente tiene varias cuentas; cada cuenta usa una moneda
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="cuentas")
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, related_name="cuentas")
    numero = models.CharField(max_length=20, unique=True, editable=False)
    saldo = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    # Muchos a Muchos: cuentas compartidas entre varios clientes
    co_titulares = models.ManyToManyField(Cliente, blank=True, related_name="cuentas_compartidas")
    activa = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero"]

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f"AW-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero} - {self.cliente}"


class Transaccion(models.Model):
    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="enviadas")
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="recibidas")
    monto = models.DecimalField(
        max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    descripcion = models.CharField(max_length=140, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "transacción"
        verbose_name_plural = "transacciones"

    def clean(self):
        if not (self.cuenta_origen_id and self.cuenta_destino_id):
            return
        if self.cuenta_origen_id == self.cuenta_destino_id:
            raise ValidationError("La cuenta de origen y la de destino deben ser distintas.")
        if self.cuenta_origen.moneda_id != self.cuenta_destino.moneda_id:
            raise ValidationError("Ambas cuentas deben usar la misma moneda.")
        if self._state.adding:
            if not (self.cuenta_origen.activa and self.cuenta_destino.activa):
                raise ValidationError("Las dos cuentas deben estar activas.")
            if self.monto is not None and self.cuenta_origen.saldo < self.monto:
                raise ValidationError("Saldo insuficiente en la cuenta de origen.")

    def save(self, *args, **kwargs):
        nueva = self._state.adding
        with transaction.atomic():
            super().save(*args, **kwargs)
            if nueva:  # los saldos solo se mueven al crear el registro
                Cuenta.objects.filter(pk=self.cuenta_origen_id).update(saldo=F("saldo") - self.monto)
                Cuenta.objects.filter(pk=self.cuenta_destino_id).update(saldo=F("saldo") + self.monto)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            destino = Cuenta.objects.select_for_update().get(pk=self.cuenta_destino_id)
            if destino.saldo < self.monto:
                raise ValidationError(
                    "No se puede revertir: la cuenta de destino ya no tiene saldo suficiente."
                )
            Cuenta.objects.filter(pk=self.cuenta_origen_id).update(saldo=F("saldo") + self.monto)
            Cuenta.objects.filter(pk=self.cuenta_destino_id).update(saldo=F("saldo") - self.monto)
            return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.monto} de {self.cuenta_origen.numero} a {self.cuenta_destino.numero}"
