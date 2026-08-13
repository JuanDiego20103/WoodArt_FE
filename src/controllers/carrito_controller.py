from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.carrito.api_carrito import APICarrito, APIErrorCarrito

carrito_bp = Blueprint('carrito', __name__)

def _carrito():
    return APICarrito(session.get('api_token'))

@carrito_bp.route('/')
def index():

    usuario = session.get("usuario")

    if not usuario:

        flash(
            "Debes iniciar sesión para ver tu carrito.",
            "error"
        )

        return redirect(
            url_for("usuarios.mostrar_login")
        )

    id_usuario = usuario["id_usuario"]

    try:

        data = _carrito().get("/carrito",params={"id_usuario": id_usuario})

        carrito = APICarrito.as_list(data)

    except APIErrorCarrito as e:

        carrito = []

        flash(
            e.message,
            "error"
        )

    return render_template(
        "carrito.html",
        carrito=carrito
    )

@carrito_bp.route('/agregar', methods=['POST'])
def agregar():

    usuario = session.get("usuario")

    if not usuario:

        return {
            "error": "Debes iniciar sesión para agregar productos al carrito"
        }, 401

    data = request.get_json()

    id_producto = data.get("id_producto")
    cantidad = data.get("cantidad", 1)

    if not id_producto:

        return {
            "error": "Producto no especificado"
        }, 400

    data["id_usuario"] = usuario["id_usuario"]

    try:

        respuesta = _carrito().post(
            "/carrito",
            data
        )

        return respuesta, 201

    except APIErrorCarrito as e:

        return {
            "error": e.message
        }, e.status_code