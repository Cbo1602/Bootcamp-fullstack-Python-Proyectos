# interfaz.py
import tkinter as tk
from tkinter import messagebox, ttk

from exepciones import ClienteError
from gestorclientes import GestorClientes


class InterfazApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Inteligente de Clientes (GIC)")
        self.root.geometry("850x600")

        # Instancia del gestor
        self.gestor = GestorClientes()

        # Construir la interfaz
        self.crear_widgets()
        self.actualizar_tabla()

    def crear_widgets(self):
        # --- TÍTULO ---
        lbl_titulo = tk.Label(
            self.root,
            text="Sistema de Gestión de Clientes",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10,
        )
        lbl_titulo.pack(fill="x")

        # --- FORMULARIO DE INGRESO ---
        frame_form = tk.LabelFrame(
            self.root, text=" Registrar Nuevo Cliente ", padx=10, pady=10
        )
        frame_form.pack(fill="x", padx=15, pady=10)

        # Fila 1: ID, Nombre, Tipo
        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e")
        self.txt_id = tk.Entry(frame_form, width=10)
        self.txt_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="e")
        self.txt_nombre = tk.Entry(frame_form, width=20)
        self.txt_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Tipo:").grid(row=0, column=4, sticky="e")
        self.combo_tipo = ttk.Combobox(
            frame_form,
            values=["Regular", "Premium", "Corporativo"],
            state="readonly",
            width=12,
        )
        self.combo_tipo.grid(row=0, column=5, padx=5, pady=5)
        self.combo_tipo.current(0)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.cambiar_etiquetas)

        # Fila 2: Email, Teléfono, Dirección
        tk.Label(frame_form, text="Email:").grid(row=1, column=0, sticky="e")
        self.txt_email = tk.Entry(frame_form, width=20)
        self.txt_email.grid(row=1, column=1, columnspan=2, sticky="w", padx=5)

        tk.Label(frame_form, text="Teléfono:").grid(row=1, column=3, sticky="e")
        self.txt_telefono = tk.Entry(frame_form, width=15)
        self.txt_telefono.grid(row=1, column=4, sticky="w", padx=5)

        tk.Label(frame_form, text="Dirección:").grid(
            row=2, column=0, sticky="e"
        )
        self.txt_direccion = tk.Entry(frame_form, width=30)
        self.txt_direccion.grid(
            row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5
        )

        # Fila 3: Campos Dinámicos (Dato1 y Dato2 según tipo de cliente)
        self.lbl_dato1 = tk.Label(frame_form, text="Puntos:")
        self.lbl_dato1.grid(row=3, column=0, sticky="e")
        self.txt_dato1 = tk.Entry(frame_form, width=15)
        self.txt_dato1.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        self.lbl_dato2 = tk.Label(frame_form, text="Dato 2:")
        self.txt_dato2 = tk.Entry(frame_form, width=15)
        # Ocultamos dato2 inicialmente (para cliente Regular)

        # Botón Agregar
        btn_agregar = tk.Button(
            frame_form,
            text="Agregar Cliente",
            bg="#27ae60",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.agregar_cliente,
        )
        btn_agregar.grid(row=3, column=4, columnspan=2, pady=5, sticky="we")

        # --- TABLA DE DATOS ---
        frame_tabla = tk.Frame(self.root)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        columnas = ("ID", "Nombre", "Email", "Teléfono", "Dirección", "Detalles")
        self.tabla = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings"
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)

        self.tabla.pack(fill="both", expand=True, side="left")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(
            frame_tabla, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # --- PANEL INFERIOR DE BOTONES ---
        frame_acciones = tk.Frame(self.root, pady=10)
        frame_acciones.pack(fill="x", padx=15)

        btn_eliminar = tk.Button(
            frame_acciones,
            text="Eliminar Seleccionado",
            bg="#c0392b",
            fg="white",
            command=self.eliminar_cliente,
        )
        btn_eliminar.pack(side="left", padx=5)

        btn_json = tk.Button(
            frame_acciones,
            text="Exportar a JSON",
            bg="#2980b9",
            fg="white",
            command=self.exportar_json,
        )
        btn_json.pack(side="right", padx=5)

        btn_csv = tk.Button(
            frame_acciones,
            text="Exportar a CSV",
            bg="#f39c12",
            fg="white",
            command=self.exportar_csv,
        )
        btn_csv.pack(side="right", padx=5)

    def cambiar_etiquetas(self, event=None):
        """Ajusta las etiquetas según el tipo de cliente seleccionado."""
        tipo = self.combo_tipo.get()

        if tipo == "Regular":
            self.lbl_dato1.config(text="Puntos:")
            self.lbl_dato2.grid_forget()
            self.txt_dato2.grid_forget()
        elif tipo == "Premium":
            self.lbl_dato1.config(text="Membresía:")
            self.lbl_dato2.config(text="% Descuento:")
            self.lbl_dato2.grid(row=3, column=2, sticky="e")
            self.txt_dato2.grid(row=3, column=3, sticky="w", padx=5)
        elif tipo == "Corporativo":
            self.lbl_dato1.config(text="Empresa:")
            self.lbl_dato2.config(text="Límite Crédito:")
            self.lbl_dato2.grid(row=3, column=2, sticky="e")
            self.txt_dato2.grid(row=3, column=3, sticky="w", padx=5)

    def agregar_cliente(self):
        try:
            # Obtener variables
            identificador = int(self.txt_id.get().strip())
            nombre = self.txt_nombre.get().strip()
            email = self.txt_email.get().strip()
            telefono = self.txt_telefono.get().strip()
            direccion = self.txt_direccion.get().strip()
            tipo = self.combo_tipo.get()
            dato1 = self.txt_dato1.get().strip()
            dato2 = self.txt_dato2.get().strip()

            # Intentar crear en el gestor
            self.gestor.crearCliente(
                tipo,
                identificador,
                nombre,
                email,
                telefono,
                direccion,
                dato1,
                dato2,
            )
            messagebox.showinfo(
                "Éxito", f"Cliente {nombre} registrado correctamente."
            )

            self.limpiar_formulario()
            self.actualizar_tabla()

        except ValueError:
            messagebox.showerror(
                "Error de Entrada",
                "El ID debe ser un número entero válido y los campos numéricos deben tener formato correcto.",
            )
        except ClienteError as e:
            messagebox.showerror("Error de Negocio", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))

    def eliminar_cliente(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning(
                "Atención", "Por favor, selecciona un cliente de la lista."
            )
            return

        # Obtener el ID de la primera columna
        valores = self.tabla.item(item_seleccionado)["values"]
        identificador = valores[0]

        if messagebox.askyesno(
            "Confirmar",
            f"¿Estás seguro de eliminar al cliente con ID {identificador}?",
        ):
            try:
                self.gestor.eliminar_cliente(identificador)
                self.actualizar_tabla()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            except ClienteError as e:
                messagebox.showerror("Error", str(e))

    def actualizar_tabla(self):
        # Limpiar la tabla actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Recargar desde la memoria del gestor
        for c in self.gestor.clientes:
            detalles = c.obtener_datos().split("|")[-1]
            self.tabla.insert(
                "",
                "end",
                values=(
                    c.getIdentificador(),
                    c.getNombre(),
                    c.getEmail(),
                    c.getTelefono(),
                    c.getDireccion(),
                    detalles,
                ),
            )

    def limpiar_formulario(self):
        self.txt_id.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_direccion.delete(0, tk.END)
        self.txt_dato1.delete(0, tk.END)
        self.txt_dato2.delete(0, tk.END)

    def exportar_json(self):
        try:
            self.gestor.guardar_clientes_json()
            messagebox.showinfo(
                "Exportación", "Clientes exportados con éxito a 'clientes.json'"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportar_csv(self):
        try:
            self.gestor.guardar_clientes_csv()
            messagebox.showinfo(
                "Exportación", "Clientes exportados con éxito a 'clientes.csv'"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()