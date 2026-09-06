"""
test_carrito.py — Suite de pruebas para el módulo de Gestión de Carrito
Tienda Online Sencilla · Universidad Estatal Amazónica · Grupo 17
Corresponde a los casos de prueba CP-01 a CP-07 documentados en el Avance 3 U3.
Framework: unittest (biblioteca estándar de Python — sin dependencias externas).
Ejecutar con: python -m unittest discover -s tests -v
"""

import unittest
from decimal import Decimal

from src.models import Producto, Carrito, Categoria, DetalleCarrito
from src.validators import (
    validar_cantidad,
    validar_precio,
    puede_agregar_al_carrito,
    validar_nombre_producto,
)


# -------------------------------------------------------------------------- #
# Pruebas unitarias — validadores
# -------------------------------------------------------------------------- #

class TestValidadorCantidad(unittest.TestCase):
    """CP-01: La cantidad debe ser un entero positivo mayor a 0."""

    def test_cantidad_valida_retorna_true(self):
        """Cantidad de 3 es válida."""
        es_valida, mensaje = validar_cantidad(3)
        self.assertTrue(es_valida)
        self.assertIn("válida", mensaje.lower())

    def test_cantidad_cero_retorna_false(self):
        """Cantidad 0 debe ser rechazada."""
        es_valida, mensaje = validar_cantidad(0)
        self.assertFalse(es_valida)
        self.assertIn("mayor a 0", mensaje)

    def test_cantidad_negativa_retorna_false(self):
        """Cantidad negativa debe ser rechazada."""
        es_valida, mensaje = validar_cantidad(-5)
        self.assertFalse(es_valida)
        self.assertIn("mayor a 0", mensaje)

    def test_cantidad_no_entera_retorna_false(self):
        """Cantidad no entera (string) debe ser rechazada."""
        es_valida, mensaje = validar_cantidad("tres")
        self.assertFalse(es_valida)
        self.assertIn("entero", mensaje.lower())

    def test_cantidad_excesiva_retorna_false(self):
        """Cantidad superior a 999 debe ser rechazada."""
        es_valida, mensaje = validar_cantidad(1000)
        self.assertFalse(es_valida)
        self.assertIn("999", mensaje)


class TestValidadorStock(unittest.TestCase):
    """CP-05: No se puede agregar al carrito más unidades de las disponibles en stock."""

    def test_stock_suficiente_retorna_true(self):
        """Con stock disponible mayor a la cantidad, se puede agregar."""
        puede, _ = puede_agregar_al_carrito(stock_disponible=10, cantidad_a_agregar=3)
        self.assertTrue(puede)

    def test_stock_agotado_retorna_false(self):
        """Producto agotado (stock=0) no puede agregarse."""
        puede, mensaje = puede_agregar_al_carrito(stock_disponible=0, cantidad_a_agregar=1)
        self.assertFalse(puede)
        self.assertIn("agotado", mensaje.lower())

    def test_cantidad_supera_stock_retorna_false(self):
        """No se puede agregar más de lo que hay en stock."""
        puede, mensaje = puede_agregar_al_carrito(stock_disponible=5, cantidad_a_agregar=10)
        self.assertFalse(puede)
        self.assertIn("solo hay 5", mensaje.lower())


# -------------------------------------------------------------------------- #
# Pruebas de integración — lógica de negocio del carrito
# -------------------------------------------------------------------------- #

class TestCarritoAgregarProducto(unittest.TestCase):
    """
    CP-02: Agregar un producto válido al carrito debe guardarse correctamente.
    CP-03: Agregar un producto agotado debe ser rechazado (RF-12).
    """

    def test_agregar_producto_disponible_exitoso(self):
        """CP-02 — Integración: producto disponible se agrega sin error."""
        categoria = Categoria("Electrónica")
        producto = Producto(nombre="Mouse Inalámbrico", precio=Decimal("25.50"), stock=15, categoria=categoria)
        carrito = Carrito()

        exito, mensaje = carrito.agregar_producto(producto, cantidad=2)

        self.assertTrue(exito)
        self.assertIn("agregado", mensaje.lower())
        self.assertEqual(len(carrito.obtener_detalles()), 1)
        self.assertEqual(carrito.obtener_detalles()[0].producto.nombre, "Mouse Inalámbrico")

    def test_agregar_producto_agotado_rechazado(self):
        """CP-03 — Integración: producto agotado debe ser rechazado (RF-12)."""
        producto = Producto(nombre="Teclado Roto", precio=Decimal("10.00"), stock=0)
        carrito = Carrito()

        exito, mensaje = carrito.agregar_producto(producto)

        self.assertFalse(exito)
        self.assertIn("agotado", mensaje.lower())
        self.assertEqual(len(carrito.obtener_detalles()), 0)

    def test_agregar_mismo_producto_incrementa_cantidad(self):
        """Integración: agregar el mismo producto dos veces incrementa la cantidad."""
        producto = Producto(nombre="Cable USB", precio=Decimal("5.00"), stock=20)
        carrito = Carrito()

        carrito.agregar_producto(producto, cantidad=2)
        carrito.agregar_producto(producto, cantidad=3)

        self.assertEqual(len(carrito.obtener_detalles()), 1)
        self.assertEqual(carrito.obtener_detalles()[0].cantidad, 5)


class TestCarritoModificarCantidad(unittest.TestCase):
    """
    CP-06: La cantidad de un producto puede modificarse correctamente (RF-11).
    """

    def test_modificar_cantidad_producto_existente(self):
        """CP-06 — Integración: cambiar cantidad de un producto en el carrito."""
        producto = Producto(nombre="Monitor LED", precio=Decimal("150.00"), stock=10)
        carrito = Carrito()
        carrito.agregar_producto(producto, cantidad=2)

        exito, mensaje = carrito.cambiar_cantidad(producto.id, nueva_cantidad=5)

        self.assertTrue(exito)
        self.assertEqual(carrito.obtener_detalles()[0].cantidad, 5)
        self.assertIn("actualizada", mensaje.lower())

    def test_cambiar_cantidad_a_cero_elimina_producto(self):
        """Integración: cambiar cantidad a 0 elimina el producto del carrito."""
        producto = Producto(nombre="Webcam HD", precio=Decimal("45.00"), stock=8)
        carrito = Carrito()
        carrito.agregar_producto(producto, cantidad=3)

        exito, mensaje = carrito.cambiar_cantidad(producto.id, nueva_cantidad=0)

        self.assertTrue(exito)
        self.assertEqual(len(carrito.obtener_detalles()), 0)

    def test_cambiar_cantidad_producto_inexistente_retorna_error(self):
        """Integración: cambiar cantidad de producto que no está en el carrito."""
        producto = Producto(nombre="Producto A", precio=Decimal("10.00"), stock=5)
        carrito = Carrito()

        exito, mensaje = carrito.cambiar_cantidad(producto.id, nueva_cantidad=3)

        self.assertFalse(exito)
        self.assertIn("no está en el carrito", mensaje.lower())


class TestCarritoEliminar(unittest.TestCase):
    """Integración: eliminar un producto del carrito funciona correctamente."""

    def test_eliminar_producto_existente(self):
        """Integración: eliminar un producto presente en el carrito."""
        producto_a = Producto(nombre="Producto A", precio=Decimal("10.00"), stock=5)
        producto_b = Producto(nombre="Producto B", precio=Decimal("20.00"), stock=5)
        carrito = Carrito()
        carrito.agregar_producto(producto_a)
        carrito.agregar_producto(producto_b)

        exito, mensaje = carrito.eliminar_producto(producto_a.id)

        self.assertTrue(exito)
        self.assertIn("eliminado", mensaje.lower())
        self.assertEqual(len(carrito.obtener_detalles()), 1)
        self.assertEqual(carrito.obtener_detalles()[0].producto.nombre, "Producto B")

    def test_eliminar_producto_inexistente_retorna_error(self):
        """Integración: eliminar un producto que no está en el carrito."""
        producto = Producto(nombre="Producto X", precio=Decimal("10.00"), stock=5)
        carrito = Carrito()

        exito, mensaje = carrito.eliminar_producto(producto.id)

        self.assertFalse(exito)
        self.assertIn("no está en el carrito", mensaje.lower())


class TestCarritoCalcularTotal(unittest.TestCase):
    """Integración: el total del carrito se calcula correctamente (RF-10)."""

    def test_calcular_total_vacio(self):
        """Carrito vacío tiene total 0."""
        carrito = Carrito()
        self.assertEqual(carrito.calcular_total(), Decimal("0.00"))

    def test_calcular_total_un_producto(self):
        """Total con un producto: precio × cantidad."""
        producto = Producto(nombre="Disco SSD", precio=Decimal("45.00"), stock=20)
        carrito = Carrito()
        carrito.agregar_producto(producto, cantidad=2)

        self.assertEqual(carrito.calcular_total(), Decimal("90.00"))

    def test_calcular_total_multiple_productos(self):
        """Total con múltiples productos: suma de subtotales."""
        producto_a = Producto(nombre="Teclado", precio=Decimal("30.00"), stock=20)
        producto_b = Producto(nombre="Mouse", precio=Decimal("15.00"), stock=20)
        producto_c = Producto(nombre="USB 32GB", precio=Decimal("8.50"), stock=20)
        carrito = Carrito()
        carrito.agregar_producto(producto_a, cantidad=1)  # 30.00
        carrito.agregar_producto(producto_b, cantidad=2)  # 30.00
        carrito.agregar_producto(producto_c, cantidad=4)  # 34.00

        self.assertEqual(carrito.calcular_total(), Decimal("94.00"))


# -------------------------------------------------------------------------- #
# Prueba de aceptación — flujo completo de agregar al carrito
# -------------------------------------------------------------------------- #

class TestCarritoAceptacion(unittest.TestCase):
    """
    CP-07 — Aceptación: El cliente agrega un producto y ve el resumen actualizado.
    Valida RF-09 (agregar al carrito) y RF-10 (ver resumen con total).
    """

    def test_flujo_completo_agregar_producto(self):
        """
        CP-07 — Aceptación: flujo completo desde que el cliente
        agrega un producto hasta que ve el resumen del carrito.
        """
        # Datos del producto
        producto = Producto(
            nombre="Auriculares Bluetooth",
            precio=Decimal("19.99"),
            stock=15,
            descripcion="Auriculares over-ear con cancelación de ruido",
        )

        # Crear carrito y agregar producto
        carrito = Carrito()
        cantidad_deseada = 2

        # Paso 1: Validar cantidad (CP-01)
        es_valida, _ = validar_cantidad(cantidad_deseada)
        self.assertTrue(es_valida)

        # Paso 2: Verificar stock (CP-05)
        puede, _ = puede_agregar_al_carrito(producto.stock, cantidad_deseada)
        self.assertTrue(puede)

        # Paso 3: Agregar al carrito (CP-02)
        exito, mensaje = carrito.agregar_producto(producto, cantidad=cantidad_deseada)
        self.assertTrue(exito)
        self.assertIn("agregado", mensaje.lower())

        # Paso 4: Verificar que el producto está en el carrito
        detalles = carrito.obtener_detalles()
        self.assertEqual(len(detalles), 1)
        self.assertEqual(detalles[0].producto.nombre, "Auriculares Bluetooth")
        self.assertEqual(detalles[0].cantidad, 2)

        # Paso 5: Verificar subtotal y total (RF-10)
        self.assertEqual(detalles[0].subtotal, Decimal("39.98"))
        self.assertEqual(carrito.calcular_total(), Decimal("39.98"))

        # Verificación final: el flujo completo funciona
        # (equivalente a que la recepcionista ve el resumen del pedido)


if __name__ == "__main__":
    unittest.main()
