from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.inventario.api_inventario import APIInventario, APIErrorInventario

inventario_bp = Blueprint('inventario', __name__)

def _inventario():
    return APIInventario(session.get('api_token'))

@inventario_bp.route('/')
def index ():
    q = request.args.get('q', '') .strip()
    try:
        data = _inventario().get('/inventario/')
        print(f"data: {data}")
        inventario = APIInventario.as_list(data)
    except APIErrorInventario as e:
            inventario = []

    print(inventario)
    return render_template('inventario/', inventario=inventario, q=q)