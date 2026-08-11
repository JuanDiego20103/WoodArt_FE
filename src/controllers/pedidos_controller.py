from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.pedidos.api_pedidos import APIPedidos, APIErrorPedidos
from src.pedidos.api_detalle_pedido import APIDetallePedido, APIErrorDetallePedido
from src.pedidos.api_pagos import APIPagos, APIErrorPagos

pedidos_bp = Blueprint('pedidos', __name__)

def _pedidos():
    return APIPedidos(session.get('api_token'))

@pedidos_bp.route('/')
def index ():
    q = request.args.get('q', '') .strip()
    try:
        data = _pedidos().get('/pedidos/')
        print(f"data: {data}")
        pedidos = APIPedidos.as_list(data)
    except APIErrorPedidos as e:
            pedidos = []

    print(pedidos)
    return render_template('pedidos/', pedidos=pedidos, q=q)