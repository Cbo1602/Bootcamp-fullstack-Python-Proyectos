# test/test_cliente.py
import sys
import unittest
from pathlib import Path

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from cliente import ClienteCorporativo, ClientePremium, ClienteRegular
from exepciones import DatoInvalidoError, EmailInvalidoError


class TestCliente(unittest.TestCase):

    def test_creacion_cliente_regular_exito(self):
        cliente = ClienteRegular(
            1, "Juan Perez", "juan@gmail.com", "123456789", "Calle 123", 100
        )
        self.assertEqual(cliente.getIdentificador(), 1)
        self.assertEqual(cliente.getNombre(), "Juan Perez")
        self.assertEqual(cliente.getPuntos_Acumulados(), 100)

    def test_email_invalido_lanza_excepcion(self):
        with self.assertRaises(EmailInvalidoError):
            ClienteRegular(
                2, "Ana Garcia", "anagmail.com", "987654321", "Av. Central", 50
            )

    def test_nombre_vacio_lanza_excepcion(self):
        with self.assertRaises(DatoInvalidoError):
            ClienteRegular(
                3, "", "contacto@empresa.com", "987654321", "Calle 45", 0
            )

    def test_cliente_premium(self):
        cliente = ClientePremium(
            4,
            "Carlos",
            "carlos@gmail.com",
            "11223344",
            "Pasaje 5",
            "Gold",
            15,
        )
        self.assertEqual(cliente.getNivelMembresia(), "Gold")
        self.assertEqual(cliente.getPorcentajeDescuento(), 15)

    def test_cliente_corporativo(self):
        cliente = ClienteCorporativo(
            5,
            "Tech Corp",
            "contacto@tech.com",
            "55667788",
            "Av. Principal",
            "Tech",
            50000,
        )
        self.assertEqual(cliente.getEmpresa(), "Tech")
        self.assertEqual(cliente.getLimiteCredito(), 50000)


if __name__ == "__main__":
    unittest.main()