# exepciones.py


class ClienteError(Exception):
    """Clase base para todas las excepciones del sistema de gestión de clientes."""

    pass


class EmailInvalidoError(ClienteError):
    """Se lanza cuando el correo electrónico no cumple con la validación requerida."""

    def __init__(self, email):
        self.message = (
            f"El formato del correo '{email}' no es válido (debe contener '@')."
        )
        super().__init__(self.message)


class ClienteNoEncontradoError(ClienteError):
    """Se lanza cuando no se encuentra un cliente con el identificador indicado."""

    def __init__(self, identificador):
        self.message = (
            f"No se encontró ningún cliente con el ID: {identificador}."
        )
        super().__init__(self.message)


class DatoInvalidoError(ClienteError):
    """Se lanza cuando un dato obligatorio está vacío o es inválido."""

    def __init__(self, campo):
        self.message = f"El campo '{campo}' es obligatorio y no puede estar vacío ni ser inválido."
        super().__init__(self.message)


class ClienteYaExisteError(ClienteError):
    """Se lanza cuando se intenta registrar un cliente con un ID que ya existe."""

    def __init__(self, identificador):
        self.message = (
            f"Ya existe un cliente registrado con el ID: {identificador}."
        )
        super().__init__(self.message)