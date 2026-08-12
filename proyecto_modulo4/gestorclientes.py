# gestorclientes.py
import csv
from datetime import datetime

# Importación de nuestros módulos
from api import ServicioExternoAPI
from archivos import GestorArchivos
from base_datos import BaseDatos
from cliente import ClienteCorporativo, ClientePremium, ClienteRegular
from exepciones import (
    ClienteNoEncontradoError,
    ClienteYaExisteError,
    DatoInvalidoError,
)


class GestorClientes:

    def __init__(self):
        self.clientes = []
        self.bd = BaseDatos()  # Maneja la conexión SQLite
        self.cargar_desde_bd()  # Carga los clientes guardados al iniciar

    def cargar_desde_bd(self):
        """Carga los clientes existentes desde SQLite a la lista en memoria."""
        registros = self.bd.cargar_todos()
        for reg in registros:
            id_cli, tipo, nom, email, tel, direc, d1, d2 = reg
            try:
                if tipo == "Regular":
                    cliente = ClienteRegular(id_cli, nom, email, tel, direc, d1)
                elif tipo == "Premium":
                    cliente = ClientePremium(
                        id_cli, nom, email, tel, direc, d1, d2
                    )
                elif tipo == "Corporativo":
                    cliente = ClienteCorporativo(
                        id_cli, nom, email, tel, direc, d1, d2
                    )

                self.clientes.append(cliente)
            except Exception as e:
                print(f"Error al cargar cliente ID {id_cli}: {e}")

    def crearCliente(
        self,
        tipo,
        identificador,
        nombre,
        email,
        telefono,
        direccion,
        dato1,
        dato2="",
    ):
        # 1. Validar email vía API
        ServicioExternoAPI.validar_email_api(email)

        # 2. Validar que no exista un cliente con el mismo ID
        if self.buscar_cliente(identificador) is not None:
            raise ClienteYaExisteError(identificador)

        # 3. Crear el objeto 'cliente' según el tipo
        if tipo == "Regular":
            cliente = ClienteRegular(
                identificador, nombre, email, telefono, direccion, dato1
            )
        elif tipo == "Premium":
            cliente = ClientePremium(
                identificador,
                nombre,
                email,
                telefono,
                direccion,
                dato1,
                dato2,
            )
        elif tipo == "Corporativo":
            cliente = ClienteCorporativo(
                identificador,
                nombre,
                email,
                telefono,
                direccion,
                dato1,
                dato2,
            )
        else:
            raise DatoInvalidoError("Tipo de Cliente")

        # 4. Guardar en la lista local y en SQLite
        self.clientes.append(cliente)
        self.bd.guardar_cliente(
            identificador,
            tipo,
            nombre,
            email,
            telefono,
            direccion,
            dato1,
            dato2,
        )

        # 5. Enviar notificación de bienvenida vía API
        ServicioExternoAPI.enviar_email_bienvenida(nombre, email)

        # 6. Registrar en el archivo de actividad
        self.guardar_actividad(f"Agregó cliente ID: {identificador}")

    def editar_cliente(
        self,
        identificador,
        tipo,
        nombre,
        email,
        telefono,
        direccion,
        dato1,
        dato2="",
    ):
        cliente = self.buscar_cliente(identificador)

        if cliente is None:
            raise ClienteNoEncontradoError(identificador)

        posicion = self.clientes.index(cliente)

        if tipo == "Regular":
            cliente_editado = ClienteRegular(
                identificador, nombre, email, telefono, direccion, dato1
            )
        elif tipo == "Premium":
            cliente_editado = ClientePremium(
                identificador,
                nombre,
                email,
                telefono,
                direccion,
                dato1,
                dato2,
            )
        elif tipo == "Corporativo":
            cliente_editado = ClienteCorporativo(
                identificador,
                nombre,
                email,
                telefono,
                direccion,
                dato1,
                dato2,
            )
        else:
            raise DatoInvalidoError("Tipo de Cliente")

        self.clientes[posicion] = cliente_editado

        # Actualizar en SQLite
        self.bd.guardar_cliente(
            identificador,
            tipo,
            nombre,
            email,
            telefono,
            direccion,
            dato1,
            dato2,
        )
        self.guardar_actividad(f"Editó cliente ID: {identificador}")

    def eliminar_cliente(self, identificador):
        cliente = self.buscar_cliente(identificador)

        if cliente is None:
            raise ClienteNoEncontradoError(identificador)

        self.clientes.remove(cliente)

        # Eliminar de SQLite
        self.bd.eliminar_cliente(identificador)
        self.guardar_actividad(f"Eliminó cliente ID: {identificador}")

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.getIdentificador() == identificador:
                return cliente
        return None

    # --- MÉTODOS DE EXPORTACIÓN Y LOGS ---
    def guardar_clientes_txt(self):
        GestorArchivos.guardar_txt(self.clientes)
        self.guardar_actividad("Generó archivo .txt")

    def guardar_clientes_csv(self):
        GestorArchivos.guardar_csv(self.clientes)
        self.guardar_actividad("Generó archivo .csv")

    def guardar_clientes_json(self):
        GestorArchivos.guardar_json(self.clientes)
        self.guardar_actividad("Generó archivo .json")

    def guardar_actividad(self, mensaje):
        fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("actividad.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"Fecha: {fecha} | Acción: {mensaje}\n")