
import csv

def calcular_factorial(n: int) -> int:

    if n == 0 or n == 1:
        return 1
    return n * calcular_factorial(n - 1)

def exportar_csv(inventario, nombre_archivo="inventario.csv"):
    
    if not inventario:
        print("No hay productos en el inventario.")
        return


    ENCABEZADOS = ("Nombre", "Categoría", "Precio", "Stock")

    try:
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(ENCABEZADOS)
            
            for producto in inventario:
                escritor.writerow([
                    producto["nombre"],
                    producto["categoria"],
                    producto["precio"],
                    producto["stock"]
                ])
        print(f"Inventario exportado exitosamente a '{nombre_archivo}'.")
    except Exception as e:
        print(f"No se logro exportar el archivo: {e}")