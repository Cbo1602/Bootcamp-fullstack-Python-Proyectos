# cliente.py
from exepciones import DatoInvalidoError, EmailInvalidoError


# Clase padre (Superclase)
class Cliente:

    def __init__(self, identificador, nombre, email, telefono, direccion):
        if not identificador:
            raise DatoInvalidoError("Identificador")

        if not nombre:
            raise DatoInvalidoError("Nombre")

        if "@" not in email:
            raise EmailInvalidoError(email)

        if not telefono:
            raise DatoInvalidoError("Teléfono")

        if not direccion:
            raise DatoInvalidoError("Dirección")

        self.__identificador = identificador
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.__direccion = direccion

    def getIdentificador(self):
        return self.__identificador

    def getNombre(self):
        return self.__nombre

    def getEmail(self):
        return self.__email

    def getTelefono(self):
        return self.__telefono

    def getDireccion(self):
        return self.__direccion

    def obtener_datos(self):
        return f"ID: {self.__identificador} | Nombre: {self.__nombre} | Email: {self.__email} | Teléfono: {self.__telefono} | Dirección: {self.__direccion}"


# Clase hija (subclase)
class ClienteRegular(Cliente):

    def __init__(
        self,
        identificador,
        nombre,
        email,
        telefono,
        direccion,
        puntos_acumulados,
    ):
        if puntos_acumulados == "":
            raise DatoInvalidoError("Puntos acumulados")

        super().__init__(identificador, nombre, email, telefono, direccion)
        self.__puntos_acumulados = puntos_acumulados

    def getPuntos_Acumulados(self):
        return self.__puntos_acumulados

    def obtener_datos(self):
        return f"{super().obtener_datos()} | Puntos acumulados: {self.__puntos_acumulados}"


# Clase hija (subclase)
class ClientePremium(Cliente):

    def __init__(
        self,
        identificador,
        nombre,
        email,
        telefono,
        direccion,
        nivel_membresia,
        porcentaje_descuento,
    ):
        if not nivel_membresia:
            raise DatoInvalidoError("Nivel de membresía")

        if porcentaje_descuento == "":
            raise DatoInvalidoError("Porcentaje de descuento")

        super().__init__(identificador, nombre, email, telefono, direccion)
        self.__nivel_membresia = nivel_membresia
        self.__porcentaje_descuento = porcentaje_descuento

    def getNivelMembresia(self):
        return self.__nivel_membresia

    def getPorcentajeDescuento(self):
        return self.__porcentaje_descuento

    def obtener_datos(self):
        return f"{super().obtener_datos()} | Nivel de Membresía: {self.__nivel_membresia} | Porcentaje de Descuento: {self.__porcentaje_descuento}"


# Clase hija (subclase)
class ClienteCorporativo(Cliente):

    def __init__(
        self,
        identificador,
        nombre,
        email,
        telefono,
        direccion,
        empresa,
        limite_credito,
    ):
        if not empresa:
            raise DatoInvalidoError("Empresa")

        if limite_credito == "":
            raise DatoInvalidoError("Límite de crédito")

        super().__init__(identificador, nombre, email, telefono, direccion)
        self.__empresa = empresa
        self.__limite_credito = limite_credito

    def getEmpresa(self):
        return self.__empresa

    def getLimiteCredito(self):
        return self.__limite_credito

    def obtener_datos(self):
        return f"{super().obtener_datos()} | Empresa: {self.__empresa} | Límite de Crédito: {self.__limite_credito}"