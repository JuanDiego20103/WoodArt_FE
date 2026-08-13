from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.usuarios.api_usuario import APIUsuario, APIError

usuarios_bp = Blueprint("usuarios", __name__)


def _usuario():
    return APIUsuario(session.get("api_token"))


# =========================
# MOSTRAR LOGIN / REGISTRO
# =========================

@usuarios_bp.route("/login", methods=["GET"])
def mostrar_login():

    return render_template("login.html")


# =========================
# INICIAR SESIÓN
# =========================

@usuarios_bp.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    data = {
        "email": email,
        "password": password
    }

    try:

        respuesta = _usuario().post(
            "/usuarios/login",
            data
        )

        session["usuario"] = respuesta["usuario"]

        flash(
            "Inicio de sesión exitoso.",
            "success"
        )

        return redirect(
            url_for("home.index")
        )

    except APIError as e:

        flash(
            e.message,
            "error"
        )

        return redirect(
            url_for("usuarios.mostrar_login")
        )

# =========================
# Cerrar sesión
# =========================

@usuarios_bp.route("/logout")
def logout():

    session.pop("usuario", None)

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("home.index")
    )


# =========================
# REGISTRAR USUARIO
# =========================

@usuarios_bp.route("/registro", methods=["POST"])
def registro():

    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    password = request.form.get("password")

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono,
        "password": password
    }

    try:

        respuesta = _usuario().post(
            "/usuarios",
            data
        )

        flash(
            "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
            "success"
        )

        return redirect(
            url_for("usuarios.mostrar_login")
        )

    except APIError as e:

        flash(
            e.message,
            "error"
        )

        return redirect(
            url_for("usuarios.mostrar_login")
        )