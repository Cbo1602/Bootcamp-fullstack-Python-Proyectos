# archivos.py
import csv
import json
from exepciones import ClienteError


class GestorArchivos:

    @staticmethod
    def guardar_txt(clientes, nombre_archivo="clientes.txt"):
        """Guarda la lista de clientes en formato de texto plano (.txt)."""
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                for cliente in clientes:
                    archivo.write(cliente.obtener_datos() + "\n")
        except Exception as e:
            raise ClienteError(f"Error al exportar a TXT: {e}")

    @staticmethod
    def guardar_csv(clientes, nombre_archivo="clientes.csv"):
        """Guarda los datos básicos de los clientes en formato CSV."""
        try:
            with open(
                nombre_archivo, "w", newline="", encoding="utf-8"
            ) as archivo:
                escritor = csv.writer(archivo, delimiter=";")
                # Encabezados
                escritor.writerow(
                    ["Identificador", "Nombre", "Email", "Teléfono", "Dirección"]
                )

                for cliente in clientes:
                    escritor.writerow(
                        [
                            cliente.getIdentificador(),
                            cliente.getNombre(),
                            cliente.getEmail(),
                            cliente.getTelefono(),
                            cliente.getDireccion(),
                        ]
                    )
        except Exception as e:
            raise ClienteError(f"Error al exportar a CSV: {e}")

    @staticmethod
    def guardar_json(clientes, nombre_archivo="clientes.json"):
        """Exporta la lista completa de clientes a un archivo JSON."""
        lista_datos = []

        for cliente in clientes:
            # Determinamos el tipo de cliente según la clase
            tipo_cliente = cliente.__class__.__name__

            datos = {
                "identificador": cliente.getIdentificador(),
                "tipo": tipo_cliente,
                "nombre": cliente.getNombre(),
                "email": cliente.getEmail(),
                "telefono": cliente.getTelefono(),
                "direccion": cliente.getDireccion(),
            }

            # Atributos específicos según la subclase
            if tipo_cliente == "ClienteRegular":
                datos["puntos_acumulados"] = cliente.getPuntos_Acumulados()
            elif tipo_cliente == "ClientePremium":
                datos["nivel_membresia"] = cliente.getNivelMembresia()
                datos["porcentaje_descuento"] = (
                    cliente.getPorcentajeDescuento()
                )
            elif tipo_cliente == "ClienteCorporativo":
                datos["empresa"] = cliente.getEmpresa()
                datos["limite_credito"] = cliente.getLimiteCredito()

            lista_datos.append(datos)

        try:
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                json.dump(lista_datos, archivo, ensure_ascii=False, indent=4)
        except Exception as e:
            raise ClienteError(f"Error al exportar a JSON: {e}")