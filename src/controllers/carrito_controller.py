from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.carrito.api_carrito import APICarrito, APIErrorCarrito

carrito_bp = Blueprint('carrito', __name__)

def _carrito():
    return APICarrito(session.get('api_token'))

@carrito_bp.route('/')
def index ():
    q = request.args.get('q', '') .strip()
    try:
        data = _carrito().get('/carrito/')
        print(f"data: {data}")
        carrito = APICarrito.as_list(data)
    except APIErrorCarrito as e:
            carrito = []

    print(carrito)
    return render_template('carrito.html/', carrito=carrito, q=q)