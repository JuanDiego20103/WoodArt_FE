from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.productos.api_productos import APIProductos, APIErrorProductos
from src.productos.api_categorias import APICategorias, APIErrorCategorias
from src.productos.api_Imagen_productos import APIImagenProductos, APIErrorImagenProductos

productos_bp = Blueprint("productos", __name__)


def _producto():
    return APIProductos(session.get("api_token"))


# ===========================
# LISTAR TODOS LOS PRODUCTOS
# ===========================
@productos_bp.route("/")
def index():

    q = request.args.get("q", "").strip()

    try:
        data = _producto().get("/productos")
        productos = APIProductos.as_list(data)

    except APIErrorProductos:
        productos = []

    return render_template(
        "productos.html",
        productos=productos,
        q=q
    )


# ===========================
# FORMULARIO NUEVO PRODUCTO
# ===========================
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

            _producto().post("/productos", data)

            flash("Producto creado correctamente", "success")

            return redirect(url_for("productos.index"))

        except APIErrorProductos as e:

            flash(e.message, "danger")

    return render_template("nuevo_producto.html")


# ===========================
# CATEGORÍAS
# ===========================

@productos_bp.route("/maderas")
def maderas():

    try:
        data = _producto().get(
            "/productos",
            params={"id_categoria": 1}
        )

        productos = APIProductos.as_list(data)

    except APIErrorProductos:
        productos = []

    return render_template(
        "Maderas.html",
        productos=productos
    )


@productos_bp.route("/muebles")
def muebles():

    try:
        data = _producto().get(
            "/productos",
            params={"id_categoria": 2}
        )

        productos = APIProductos.as_list(data)

    except APIErrorProductos:
        productos = []

    return render_template(
        "Muebles.html",
        productos=productos
    )


@productos_bp.route("/herrajes")
def herrajes():

    try:
        data = _producto().get(
            "/productos",
            params={"id_categoria": 3}
        )

        productos = APIProductos.as_list(data)

    except APIErrorProductos:
        productos = []

    return render_template(
        "Herrajes.html",
        productos=productos
    )


@productos_bp.route("/pisos")
def pisos():

    try:
        data = _producto().get(
            "/productos",
            params={"id_categoria": 4}
        )

        productos = APIProductos.as_list(data)

    except APIErrorProductos:
        productos = []

    return render_template(
        "Pisos.html",
        productos=productos
    )


@productos_bp.route("/puertas")
def puertas():

    try:
        data = _producto().get(
            "/productos",
            params={"id_categoria": 5}
        )

        productos = APIProductos.as_list(data)

    except APIErrorProductos:
        productos = []

    return render_template(
        "Puertas.html",
        productos=productos
    )