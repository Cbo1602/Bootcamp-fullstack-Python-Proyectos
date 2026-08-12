

def leer_numero(mensaje, es_entero=False):

    while True:
        try:
            entrada = input(mensaje)
            valor = int(entrada) if es_entero else float(entrada)
            if valor < 0:
                print("El número debe ser mayor o igual a 0.")
                continue
            return valor
        except ValueError:
            print("Por favor, ingrese un número válido, mayor o igual a 0.")