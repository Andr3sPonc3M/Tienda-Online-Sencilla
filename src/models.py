"""
models.py — Modelos del módulo de Gestión de Carrito
Tienda Online Sencilla · Universidad Estatal Amazónica · Grupo 17
Responde a: RF-09, RF-10, RF-11, RF-12 del SRS
Usa únicamente la biblioteca estándar de Python (sin dependencias externas).
"""

from decimal import Decimal
from typing import Optional, List, Tuple


class Categoria:
    """Categoría de producto: Electrónica, Ropa, Hogar, Alimentos."""
    _contador = 0

    def __init__(self, nombre: str):
        Categoria._contador += 1
        self.id = Categoria._contador
        self.nombre = nombre

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}')"

    def __eq__(self, other):
        if not isinstance(other, Categoria):
            return False
        return self.nombre == other.nombre


class Producto:
    """Producto del catálogo de la tienda en línea."""
    _contador = 0

    def __init__(
        self,
        nombre: str,
        precio: Decimal,
        stock: int = 0,
        categoria: Optional[Categoria] = None,
        descripcion: str = "",
        imagen_url: str = "",
    ):
        Producto._contador += 1
        self.id = Producto._contador
        self.nombre = nombre
        self.precio = Decimal(str(precio))
        self.stock = stock
        self.categoria = categoria
        self.descripcion = descripcion
        self.imagen_url = imagen_url
        self.disponible = stock > 0

    def esta_agotado(self) -> bool:
        """Retorna True si el stock es 0."""
        return self.stock <= 0

    def __repr__(self):
        return (
            f"Producto(id={self.id}, nombre='{self.nombre}', "
            f"precio={self.precio}, stock={self.stock})"
        )


class DetalleCarrito:
    """Línea de detalle dentro de un carrito: producto + cantidad."""
    _contador = 0

    def __init__(self, producto: Producto, cantidad: int = 1):
        DetalleCarrito._contador += 1
        self.id = DetalleCarrito._contador
        self.producto = producto
        self.cantidad = cantidad

    @property
    def subtotal(self) -> Decimal:
        """Calcula el subtotal (precio unitario × cantidad)."""
        return self.producto.precio * self.cantidad

    def __repr__(self):
        return f"DetalleCarrito(id={self.id}, producto={self.producto.nombre}, cantidad={self.cantidad})"


class Carrito:
    """Carrito de compras asociado a un cliente."""
    _contador = 0

    def __init__(self):
        Carrito._contador += 1
        self.id = Carrito._contador
        self._detalles: List[DetalleCarrito] = []

    def agregar_producto(self, producto: Producto, cantidad: int = 1) -> Tuple[bool, str]:
        """
        Agrega un producto al carrito o actualiza la cantidad si ya existe.
        No permite agregar productos agotados (RF-12).
        Retorna (exito: bool, mensaje: str).
        CP-02: Producto disponible se agrega al carrito.
        CP-03: Producto agotado es rechazado.
        """
        if producto.esta_agotado():
            return False, "El producto está agotado y no puede agregarse al carrito."

        for item in self._detalles:
            if item.producto.id == producto.id:
                item.cantidad += cantidad
                return True, f"Cantidad actualizada a {item.cantidad} unidades."

        nuevo_item = DetalleCarrito(producto=producto, cantidad=cantidad)
        self._detalles.append(nuevo_item)
        return True, "Producto agregado correctamente al carrito."

    def obtener_detalles(self) -> List[DetalleCarrito]:
        """Retorna todos los detalles del carrito."""
        return list(self._detalles)

    def calcular_total(self) -> Decimal:
        """Calcula el total general del carrito (RF-10)."""
        total = Decimal("0.00")
        for item in self._detalles:
            total += item.subtotal
        return total

    def cambiar_cantidad(self, producto_id: int, nueva_cantidad: int) -> Tuple[bool, str]:
        """
        Modifica la cantidad de un producto o lo elimina si la cantidad es 0.
        RF-11: El total se actualiza automáticamente.
        Retorna (exito: bool, mensaje: str).
        CP-06: La cantidad de un producto puede modificarse.
        """
        for item in self._detalles:
            if item.producto.id == producto_id:
                if nueva_cantidad <= 0:
                    self._detalles.remove(item)
                    return True, "Producto eliminado del carrito."
                item.cantidad = nueva_cantidad
                return True, f"Cantidad actualizada a {nueva_cantidad}."
        return False, "El producto no está en el carrito."

    def eliminar_producto(self, producto_id: int) -> Tuple[bool, str]:
        """
        Elimina un producto del carrito.
        RF-11: Eliminar un producto del carrito.
        Retorna (exito: bool, mensaje: str).
        """
        for item in self._detalles:
            if item.producto.id == producto_id:
                self._detalles.remove(item)
                return True, "Producto eliminado del carrito."
        return False, "El producto no está en el carrito."

    def producto_existe(self, producto_id: int) -> bool:
        """Retorna True si el producto ya está en el carrito."""
        return any(item.producto.id == producto_id for item in self._detalles)

    def __repr__(self):
        return f"Carrito(id={self.id}, items={len(self._detalles)}, total={self.calcular_total()})"
