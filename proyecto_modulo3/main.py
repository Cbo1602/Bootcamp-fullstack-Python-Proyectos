
import funciones as fn
import utilidades as util
from validaciones import leer_numero

def menu():

    inventario = []

    while True:
        print("\n=== SISTEMA DE GESTIÓN DE INVENTARIOS ===")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto")
        print("4. Modificar producto")
        print("5. Eliminar producto")
        print("6. Mostrar categorías únicas")
        print("7. Calcular factorial (Recursividad)")
        print("8. Exportar a CSV")
        print("9. Salir")

        opcion = input("Seleccione una opción (1-9): ").strip()

        if opcion == "1":
            fn.agregar_producto(inventario)
        elif opcion == "2":
            fn.mostrar_producto(inventario)
        elif opcion == "3":
            fn.buscar_producto(inventario)
        elif opcion == "4":
            fn.modificar_producto(inventario)
        elif opcion == "5":
            fn.eliminar_producto(inventario)
        elif opcion == "6":
            fn.mostrar_categoria(inventario)
        elif opcion == "7":
            n = int(leer_numero ("Ingrese número entero para factorial: ", es_entero=True))
            res = util.calcular_factorial(n)
            print(f"🔢 El factorial de {n} es: {res}")
        elif opcion == "8":
            util.exportar_csv(inventario)
        elif opcion == "9":
            print("Saliendo del programa... ¡Hasta luego!")
            break
        else:
            print("Intente de nuevo.")

if __name__ == "__main__":
    menu()