from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Cuenta, Moneda, Transaccion


class BaseTest(TestCase):
    def setUp(self):
        self.moneda = Moneda.objects.create(codigo="CLP", nombre="Peso chileno", simbolo="$")
        self.ana = Cliente.objects.create(nombre="Ana García", email="ana@example.com")
        self.luis = Cliente.objects.create(nombre="Luis Pérez", email="luis@example.com")
        self.c1 = Cuenta.objects.create(cliente=self.ana, moneda=self.moneda, saldo=Decimal("500.00"))
        self.c2 = Cuenta.objects.create(cliente=self.luis, moneda=self.moneda, saldo=Decimal("50.00"))


class ModeloTests(BaseTest):
    def test_numero_de_cuenta_se_genera(self):
        self.assertTrue(self.c1.numero.startswith("AW-"))

    def test_transferencia_actualiza_saldos(self):
        Transaccion.objects.create(cuenta_origen=self.c1, cuenta_destino=self.c2, monto=Decimal("120.00"))
        self.c1.refresh_from_db()
        self.c2.refresh_from_db()
        self.assertEqual(self.c1.saldo, Decimal("380.00"))
        self.assertEqual(self.c2.saldo, Decimal("170.00"))

    def test_saldo_insuficiente(self):
        t = Transaccion(cuenta_origen=self.c2, cuenta_destino=self.c1, monto=Decimal("999.00"))
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_misma_cuenta_no_permitida(self):
        t = Transaccion(cuenta_origen=self.c1, cuenta_destino=self.c1, monto=Decimal("10.00"))
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_eliminar_transaccion_revierte_saldos(self):
        t = Transaccion.objects.create(cuenta_origen=self.c1, cuenta_destino=self.c2, monto=Decimal("100.00"))
        t.delete()
        self.c1.refresh_from_db()
        self.c2.refresh_from_db()
        self.assertEqual(self.c1.saldo, Decimal("500.00"))
        self.assertEqual(self.c2.saldo, Decimal("50.00"))

    def test_email_de_cliente_es_unico(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nombre="Otra Ana", email="ana@example.com")


class VistaTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user("demo", password="Clave-Segura-123")

    def test_vistas_requieren_login(self):
        for nombre in ["inicio", "cliente_list", "cuenta_list", "transaccion_list", "reportes"]:
            r = self.client.get(reverse(f"gestion:{nombre}"))
            self.assertEqual(r.status_code, 302)
            self.assertIn("/accounts/login/", r.url)

    def test_listados_y_reportes_cargan(self):
        self.client.login(username="demo", password="Clave-Segura-123")
        Transaccion.objects.create(cuenta_origen=self.c1, cuenta_destino=self.c2, monto=Decimal("150.00"))
        for nombre in ["inicio", "cliente_list", "cuenta_list", "transaccion_list", "reportes"]:
            r = self.client.get(reverse(f"gestion:{nombre}"))
            self.assertEqual(r.status_code, 200, nombre)

    def test_crud_de_cliente(self):
        self.client.login(username="demo", password="Clave-Segura-123")
        r = self.client.post(reverse("gestion:cliente_create"),
                             {"nombre": "Marta", "email": "marta@example.com", "telefono": "123456789"})
        self.assertEqual(r.status_code, 302)
        marta = Cliente.objects.get(email="marta@example.com")
        self.client.post(reverse("gestion:cliente_update", args=[marta.pk]),
                         {"nombre": "Marta R.", "email": "marta@example.com", "telefono": ""})
        marta.refresh_from_db()
        self.assertEqual(marta.nombre, "Marta R.")
        self.client.post(reverse("gestion:cliente_delete", args=[marta.pk]))
        self.assertFalse(Cliente.objects.filter(pk=marta.pk).exists())

    def test_cliente_con_cuentas_no_se_elimina(self):
        self.client.login(username="demo", password="Clave-Segura-123")
        self.client.post(reverse("gestion:cliente_delete", args=[self.ana.pk]))
        self.assertTrue(Cliente.objects.filter(pk=self.ana.pk).exists())
