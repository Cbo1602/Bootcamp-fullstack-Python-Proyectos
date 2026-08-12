# Gestor Inteligente de Clientes (GIC) 🚀

Sistema de administración, clasificación y gestión de clientes desarrollado en Python como parte del Proyecto Integrador del Módulo 4.

## 📌 Descripción

El **Gestor Inteligente de Clientes (GIC)** es una aplicación con interfaz gráfica (Tkinter) que permite administrar distintos tipos de clientes (Regular, Premium y Corporativo), garantizando la persistencia de datos mediante **SQLite** y archivos de exportación en formatos **CSV**, **JSON** y **TXT**. 

Además, integra servicios de **API REST** para la validación automática de correos electrónicos y el envío simulado de notificaciones de bienvenida.

---

## ✨ Características Principales

- **Programación Orientada a Objetos (POO):** Uso de herencia, encapsulamiento, polimorfismo y clases abstractas.
- **Tipos de Clientes:**
  - `ClienteRegular`: Puntos acumulados.
  - `ClientePremium`: Nivel de membresía y porcentaje de descuento.
  - `ClienteCorporativo`: Nombre de empresa y límite de crédito.
- **Persistencia de Datos:** Conexión relacional con SQLite (`clientes.db`).
- **Exportación de Reportes:** Generación automática de archivos `.csv`, `.json` y `.txt`.
- **Integración con APIs externas:** Validación de correos y simulador de envíos HTTP.
- **Manejo de Excepciones:** Errores personalizados para clientes duplicados, no encontrados o correos inválidos.
- **Pruebas Unitarias:** Cobertura de tests automatizados ejecutados con el módulo nativo `unittest`.
- **Registro de Actividad (Log):** Auditoría histórica de acciones en `actividad.txt`.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** Tkinter
- **Base de Datos:** SQLite3
- **Pruebas Unitarias:** `unittest`
- **Modelado UML:** PlantUML / Mermaid

---

## 📁 Estructura del Proyecto

```text
proyecto_modulo4/
├── test/
│   ├── test_cliente.py     # Pruebas unitarias para las clases de Cliente
│   └──