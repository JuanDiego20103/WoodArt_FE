from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.productos.api_productos import APIProductos, APIErrorProductos
from src.productos.api_categorias import APICategorias, APIErrorCategorias
from src.productos.api_Imagen_productos import APIImagenProductos, APIErrorImagenProductos


productos_bp = Blueprint("productos", __name__)


def _producto():
    return APIProductos(session.get("api_token"))


# =========================================================
# FUNCIÓN PARA OBTENER PRODUCTOS PAGINADOS
# =========================================================

def obtener_productos(page=1, id_categoria=None):

    try:

        params = {
            "page": page,
            "per_page": 8
        }

        # Si estamos dentro de una categoría
        if id_categoria:
            params["id_categoria"] = id_categoria

        data = _producto().get(
            "/productos",
            params=params
        )

        # El backend nuevo devuelve un diccionario
        if isinstance(data, dict):

            productos = data.get("productos", [])

            pagina_actual = data.get("pagina", 1)

            total_paginas = data.get("total_paginas", 1)

            total_productos = data.get("total_productos", 0)

        else:

            # Por si el backend todavía devuelve una lista
            productos = data if isinstance(data, list) else []

            pagina_actual = page

            total_productos = len(productos)

            total_paginas = 1

        return (
            productos,
            pagina_actual,
            total_paginas,
            total_productos
        )

    except APIErrorProductos:

        return [], 1, 1, 0


# =========================================================
# LISTAR TODOS LOS PRODUCTOS
# =========================================================

@productos_bp.route("/")
def index():

    q = request.args.get("q", "").strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    (
        productos,
        pagina_actual,
        total_paginas,
        total_productos
    ) = obtener_productos(page)

    return render_template(
        "productos.html",
        productos=productos,
        q=q,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        total_productos=total_productos,
        endpoint="productos.index"
    )


# =========================================================
# FORMULARIO NUEVO PRODUCTO
# =========================================================

@productos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    if request.method == "POST":

        data = {
            "nombre": request.form.get("nombre"),
            "descripcion": request.form.get("descripcion"),
            "precio": float(request.form.get("precio")),
            "stock": int(request.form.get("stock")),
            "material": request.form.get("material"),
            "color": request.form.get("color"),
            "imagen_principal": request.form.get("imagen_principal"),
            "dimensiones": request.form.get("dimensiones"),
            "peso": float(request.form.get("peso")),
            "id_categoria": int(request.form.get("id_categoria"))
        }

        try:

            _producto().post(
                "/productos",
                data
            )

            flash(
                "Producto creado correctamente",
                "success"
            )

            return redirect(
                url_for("productos.index")
            )

        except APIErrorProductos as e:

            flash(
                e.message,
                "danger"
            )

    return render_template(
        "nuevo_producto.html"
    )


# =========================================================
# MADERAS
# =========================================================

@productos_bp.route("/maderas")
def maderas():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    (
        productos,
        pagina_actual,
        total_paginas,
        total_productos
    ) = obtener_productos(
        page,
        id_categoria=1
    )

    return render_template(
        "Maderas.html",
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        total_productos=total_productos,
        endpoint="productos.maderas"
    )


# =========================================================
# MUEBLES
# =========================================================

@productos_bp.route("/muebles")
def muebles():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    (
        productos,
        pagina_actual,
        total_paginas,
        total_productos
    ) = obtener_productos(
        page,
        id_categoria=2
    )

    return render_template(
        "Muebles.html",
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        total_productos=total_productos,
        endpoint="productos.muebles"
    )


# =========================================================
# HERRAJES
# =========================================================

@productos_bp.route("/herrajes")
def herrajes():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    (
        productos,
        pagina_actual,
        total_paginas,
        total_productos
    ) = obtener_productos(
        page,
        id_categoria=3
    )

    return render_template(
        "Herrajes.html",
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        total_productos=total_productos,
        endpoint="productos.herrajes"
    )


# =========================================================
# PISOS
# =========================================================

@productos_bp.route("/pisos")
def pisos():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    (
        productos,
        pagina_actual,
        total_paginas,
        total_productos
    ) = obtener_productos(
        page,
        id_categoria=4
    )

    return render_template(
        "Pisos.html",
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        total_productos=total_productos,
        endpoint="productos.pisos"
    )


# =========================================================
# PUERTAS
# =========================================================

@productos_bp.route("/puertas")
def puertas():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    (
        productos,
        pagina_actual,
        total_paginas,
        total_productos
    ) = obtener_productos(
        page,
        id_categoria=5
    )

    return render_template(
        "Puertas.html",
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        total_productos=total_productos,
        endpoint="productos.puertas"
    )