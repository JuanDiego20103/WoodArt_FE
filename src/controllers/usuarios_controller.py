from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.usuarios.api_usuario import APIUsuario, APIError
from src.usuarios.api_direccion import APIDireccion, APIErrorDireccion

usuarios_bp = Blueprint('usuarios', __name__)

def _usuario():
    return APIUsuario(session.get('api_token'))

@usuarios_bp.route('')
def index ():
    q = request.args.get('q', '') .strip()
    try:
        data = _usuario().get('/usuarios')
        print(f"data: {data}")
        usuarios = APIUsuario.as_list(data)
    except APIError as e:
            usuarios = []

    print(usuarios)
    return render_template('login.html', usuarios=usuarios, q=q)

