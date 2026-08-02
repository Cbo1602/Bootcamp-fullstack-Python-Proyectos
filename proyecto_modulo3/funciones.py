
from validaciones import leer_numero_positivo

def agregar_producto(inventario):
    print("\n=== AGREGAR PRODUCTO ===")
    nombre = input("Ingrese el nombre del producto: ").strip()
    categoria = input("Ingrese la categoría: ").strip()
    
    
    precio = leer_numero_positivo("Ingrese el precio: ", es_entero=False)
    stock = leer_numero_positivo("Ingrese el stock: ", es_entero=True)

    producto = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock
    }

    inventario.append(producto)
    print("\n Producto agregado exitosamente.")

def mostrar_producto(inventario):
    if not inventario:
        print("No hay productos registrados.")
        return

    print("\n=== LISTA DE PRODUCTOS ===")
    for producto in inventario:
        print(f"Nombre:    {producto['nombre']}")
        print(f"Categoría: {producto['categoria']}")
        print(f"Precio:    ${producto['precio']:.2f}")
        print(f"Stock:     {producto['stock']}")
        print("-" * 25)

def buscar_producto(inventario):
    nombre = input("Ingrese el nombre del producto a buscar: ").strip().lower()

    for producto in inventario:
        if producto["nombre"].lower() == nombre:
            print("\n=== PRODUCTO ENCONTRADO ===")
            print(f"Nombre:    {producto['nombre']}")
            print(f"Categoría: {producto['categoria']}")
            print(f"Precio:$   {producto['precio']:.2f}")
            print(f"Stock:     {producto['stock']}")
            return

    print("Producto NO encontrado.")

def modificar_producto(inventario):
    nombre = input("Ingrese el nombre del producto a modificar: ").strip().lower()

    for producto in inventario:
        if producto["nombre"].lower() == nombre:
            print(f"\nModificando '{producto['nombre']}':")
            producto["nombre"] = input("Nuevo nombre: ").strip()
            producto["categoria"] = input("Nueva categoría: ").strip()
            producto["precio"] = leer_numero_positivo("Nuevo precio: ", es_entero=False)
            producto["stock"] = leer_numero_positivo("Nuevo stock: ", es_entero=True)
            print("Producto modificado correctamente.")
            return

    print("Producto NO ENCONTRADO.")

def eliminar_producto(inventario):
    nombre = input("Ingrese el nombre del producto a eliminar: ").strip().lower()

    for i, producto in enumerate(inventario):
        if producto["nombre"].lower() == nombre:
            eliminado = inventario.pop(i)
            print(f"El producto '{eliminado['nombre']}' fue eliminado.")
            return

    print("Producto NO encontrado.")

def mostrar_categoria(inventario):
    
    if not inventario:
        print("No hay productos registradas.")
        return

    categorias_unicas = {prod["categoria"].capitalize() for prod in inventario}
    
    print("\n=== CATEGORÍAS DISPONIBLES ===")
    for cat in categorias_unicas:
        print(f"- {cat}")