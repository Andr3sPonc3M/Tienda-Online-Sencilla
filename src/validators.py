"""
validators.py — Validadores del módulo de Gestión de Carrito
Tienda Online Sencilla · Universidad Estatal Amazónica · Grupo 17
Responde a: RF-09, RF-10, RF-11, RF-12 del SRS
Usa únicamente la biblioteca estándar de Python (sin dependencias externas).
"""

from decimal import Decimal


def validar_cantidad(cantidad):
    """
    Valida que la cantidad sea un entero positivo mayor a 0.
    CP-01: La cantidad debe ser un entero positivo mayor a 0.
    Retorna (es_valida: bool, mensaje: str).
    """
    if not isinstance(cantidad, int):
        return False, "La cantidad debe ser un número entero."
    if cantidad <= 0:
        return False, "La cantidad debe ser mayor a 0."
    if cantidad > 999:
        return False, "La cantidad no puede superar 999 unidades."
    return True, "Cantidad válida."


def validar_precio(precio):
    """
    Valida que el precio sea un valor decimal positivo.
    Retorna (es_valido: bool, mensaje: str).
    """
    try:
        precio_dec = Decimal(str(precio))
    except Exception:
        return False, "El precio debe ser un valor numérico."
    if precio_dec <= 0:
        return False, "El precio debe ser mayor a 0."
    if precio_dec > Decimal("999999.99"):
        return False, "El precio supera el límite permitido."
    return True, "Precio válido."


def puede_agregar_al_carrito(stock_disponible, cantidad_a_agregar):
    """
    Verifica si un producto puede agregarse al carrito según su stock.
    CP-05: No se puede agregar más unidades que el stock disponible.
    Retorna (puede: bool, mensaje: str).
    """
    if stock_disponible <= 0:
        return False, "El producto está agotado."
    if cantidad_a_agregar > stock_disponible:
        return False, (
            f"Solo hay {stock_disponible} unidades disponibles. "
            f"No se pueden agregar {cantidad_a_agregar}."
        )
    return True, "Stock disponible suficiente."


def validar_nombre_producto(nombre):
    """
    Valida que el nombre del producto no esté vacío y tenga una longitud adecuada.
    Retorna (es_valido: bool, mensaje: str).
    """
    if not nombre or not nombre.strip():
        return False, "El nombre del producto no puede estar vacío."
    if len(nombre.strip()) < 3:
        return False, "El nombre del producto debe tener al menos 3 caracteres."
    if len(nombre) > 200:
        return False, "El nombre del producto no puede superar los 200 caracteres."
    return True, "Nombre válido."
