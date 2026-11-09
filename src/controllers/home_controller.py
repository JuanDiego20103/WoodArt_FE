from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from src.productos.api_productos import APIProductos, APIErrorProductos

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():

    # Productos destacados: los primeros 4 del catálogo
    try:
        data = APIProductos(session.get("api_token")).get(
            "/productos",
            params={"page": 1, "per_page": 4}
        )
        destacados = data.get("productos", []) if isinstance(data, dict) else (data or [])

    except APIErrorProductos:
        destacados = []

    return render_template('index.html', destacados=destacados)
