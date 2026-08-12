# test/test_gestor.py
import os
import sys
import unittest
from pathlib import Path

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from exepciones import ClienteNoEncontradoError, ClienteYaExisteError
from gestorclientes import GestorClientes


class TestGestorClientes(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        self.gestor = GestorClientes()
        self.gestor.clientes = []  # Limpiamos la lista en memoria para el test

    def test_crear_cliente_exito(self):
        self.gestor.crearCliente(
            "Regular",
            999,
            "Test User",
            "test@gmail.com",
            "1234",
            "Direccion Test",
            10,
        )
        cliente = self.gestor.buscar_cliente(999)
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.getNombre(), "Test User")

    def test_crear_cliente_duplicado_error(self):
        self.gestor.crearCliente(
            "Regular",
            888,
            "User 1",
            "user1@gmail.com",
            "1234",
            "Direccion",
            5,
        )
        with self.assertRaises(ClienteYaExisteError):
            self.gestor.crearCliente(
                "Regular",
                888,
                "User 2",
                "user2@gmail.com",
                "5678",
                "Otra Dir",
                10,
            )

    def test_eliminar_cliente_inexistente_error(self):
        with self.assertRaises(ClienteNoEncontradoError):
            self.gestor.eliminar_cliente(99999)

    def tearDown(self):
        """Limpieza tras las pruebas."""
        if self.gestor.buscar_cliente(999):
            try:
                self.gestor.eliminar_cliente(999)
            except Exception:
                pass
        if self.gestor.buscar_cliente(888):
            try:
                self.gestor.eliminar_cliente(888)
            except Exception:
                pass


if __name__ == "__main__":
    unittest.main()