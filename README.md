# 🛒 Tienda Online Sencilla — Grupo 17

**Módulo implementado:** Gestión de Carrito de Compras

**Stack tecnológico:** Python 3.12 + Biblioteca estándar (sin dependencias externas)

**Integrantes:**
- Ponce Maldonado Andrés Rafael — Líder de análisis
- Quiñonez Quintero Tiffany Fernanda — Analista de procesos
- Pineda Songor Manuel Alexander — Documentador ágil

**Docente:** Ing. Hermes Darío Sánchez Bermeo, Mg.

---

## Descripción del proyecto

La **Tienda Online Sencilla** es una aplicación web que permite a los clientes explorar un catálogo de productos, agregar artículos a un carrito de compras y realizar pedidos con entrega a domicilio. El sistema también incluye un panel de administración para que los vendedores gestionen el inventario y el estado de los pedidos.

En la **Unidad 3** se implementó el módulo de **Gestión de Carrito de Compras**, que responde a los siguientes requerimientos funcionales del SRS:

- **RF-09:** Agregar productos al carrito desde el catálogo o la página de detalle.
- **RF-10:** Ver el resumen del carrito con imagen, nombre, precio unitario, cantidad y subtotal por producto, más el total general.
- **RF-11:** Modificar la cantidad de cada producto o eliminarlo del carrito. El total se actualiza automáticamente.
- **RF-12:** No permitir agregar productos agotados al carrito.

---

## Flujo de ramas (GitHub Flow)

```
main (rama estable, siempre funcional)
 │
 └── feature/gestion-carrito (rama de trabajo del módulo)
```

### ¿Cómo trabajamos?

1. Se trabaja siempre en una rama de funcionalidad (ejemplo: `feature/gestion-carrito`).
2. Los commits son pequeños y con mensajes descriptivos: *"Agrega validación de stock en el carrito"*.
3. Se abre un **Pull Request (PR)** para fusionar a `main`.
4. El pipeline de CI ejecuta las pruebas automáticamente en cada push y en cada PR.
5. Solo se fusiona a `main` cuando el pipeline está en verde (✔).

### Comandos principales

```bash
# Crear y cambiar a la rama de trabajo
git checkout -b feature/gestion-carrito

# Guardar cambios con mensaje descriptivo
git add .
git commit -m "Agrega función de agregar producto al carrito"

# Subir la rama al repositorio
git push origin feature/gestion-carrito

# En GitHub: abrir Pull Request para fusionar a main
```

---

## Estructura del repositorio

```
tienda-online-sencilla/
├── README.md
├── .gitignore
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml          ← Pipeline de CI con GitHub Actions
├── src/
│   ├── __init__.py
│   ├── models.py            ← Modelos: Producto, Carrito, DetalleCarrito
│   └── validators.py       ← Validadores: cantidad, stock, precio
└── tests/
    ├── __init__.py
    └── test_carrito.py      ← Suite de pruebas (unitarias, integración, aceptación)
```

---

## Pipeline de CI

El pipeline se ejecuta automáticamente con **GitHub Actions** en cada push y pull request a la rama `main`. El workflow está definido en `.github/workflows/ci.yml` e incluye:

1. Checkout del código
2. Configuración de Python 3.12
3. Ejecución de pruebas con `unittest` (biblioteca estándar, sin dependencias externas)
4. Verificación de resultados

**Estado del pipeline:** (ver en la pestaña **Actions** de tu repositorio en GitHub)

---

## Ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/grupo17-uea/tienda-online-sencilla.git
cd tienda-online-sencilla

# 2. Ejecutar las pruebas
python3 -m unittest discover -s tests -v
```

---

## Casos de prueba documentados (Avance 3 U3)

| ID  | Nivel       | Descripción                                                    | Requerimiento |
|-----|-------------|----------------------------------------------------------------|---------------|
| CP-01 | Unitaria   | La cantidad debe ser un entero positivo mayor a 0.             | RF-11         |
| CP-02 | Integración| Producto disponible se agrega al carrito sin error.             | RF-09         |
| CP-03 | Integración| Producto agotado es rechazado al intentar agregarlo.            | RF-12         |
| CP-04 | Unitaria   | La cantidad no entera es rechazada.                            | RF-11         |
| CP-05 | Unitaria   | No se puede agregar más unidades que el stock disponible.      | RF-12         |
| CP-06 | Integración| La cantidad de un producto puede modificarse en el carrito.     | RF-11         |
| CP-07 | Aceptación| El cliente agrega un producto y ve el resumen actualizado.     | RF-09, RF-10  |

**Caso más crítico:** CP-02 — Si un producto no se guarda en el carrito, el módulo pierde su función principal.

---

*Universidad Estatal Amazónica · Ingeniería de Software · Unidad 3 · Grupo 17*
