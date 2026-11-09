from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.admin.api_admin import APIAdmin, APIErrorAdmin
from src.config.tienda import limpiar_cache_tienda

admin_bp = Blueprint("admin", __name__)


def _api():
    return APIAdmin(session.get("api_token"))


def _es_admin():
    usuario = session.get("usuario")
    return bool(usuario and usuario.get("rol") == "admin" and session.get("api_token"))


def _cerrar_sesion():
    session.pop("usuario", None)
    session.pop("api_token", None)


# =========================================================
# PROTECCIÓN DE RUTAS
# =========================================================

def admin_required(f):

    @wraps(f)
    def decorada(*args, **kwargs):

        if not _es_admin():

            if session.get("usuario"):
                flash("Necesitas una cuenta de administrador para entrar al panel.", "error")
            else:
                flash("Inicia sesión como administrador para continuar.", "error")

            return redirect(url_for("admin.login"))

        return f(*args, **kwargs)

    return decorada


def _manejar_error_api(e):
    """
    Si el token venció o ya no es admin, se cierra la sesión.
    Devuelve una redirección o None si el error es de otro tipo.
    """

    if e.status_code in (401, 403):
        _cerrar_sesion()
        flash("Tu sesión expiró o ya no tienes permisos. Inicia sesión de nuevo.", "error")
        return redirect(url_for("admin.login"))

    return None


# =========================================================
# FILTROS PARA LAS PLANTILLAS
# =========================================================

@admin_bp.app_template_filter("cop")
def formato_cop(valor):
    """250000 -> $250.000"""
    try:
        return "$" + f"{float(valor):,.0f}".replace(",", ".")
    except (TypeError, ValueError):
        return "$0"


@admin_bp.app_template_filter("cop_corto")
def formato_cop_corto(valor):
    """28771000 -> $28,8 M"""
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return "$0"

    if valor >= 1_000_000:
        return "$" + f"{valor / 1_000_000:.1f}".replace(".", ",") + " M"

    if valor >= 1_000:
        return "$" + f"{valor / 1_000:.0f}" + " mil"

    return formato_cop(valor)


# =========================================================
# LOGIN DE ADMINISTRADORES
# =========================================================

@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        if _es_admin():
            return redirect(url_for("admin.dashboard"))

        return render_template("admin/login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    try:
        respuesta = APIAdmin().post(
            "/usuarios/login",
            {"email": email, "password": password}
        )

    except APIErrorAdmin as e:
        flash(e.message, "error")
        return render_template("admin/login.html", email=email), 401

    usuario = respuesta.get("usuario", {})

    if usuario.get("rol") != "admin":
        flash("Esta cuenta no tiene permisos de administrador.", "error")
        return render_template("admin/login.html", email=email), 403

    session["usuario"] = usuario
    session["api_token"] = respuesta.get("access_token")

    flash(f"Bienvenido al panel, {usuario.get('nombre', '')}.", "success")

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/logout")
def logout():

    _cerrar_sesion()
    flash("Cerraste sesión del panel de administración.", "success")

    return redirect(url_for("admin.login"))


# =========================================================
# ANALÍTICAS
# =========================================================

@admin_bp.route("/")
@admin_required
def dashboard():

    try:
        datos = _api().get("/admin/estadisticas")

    except APIErrorAdmin as e:
        redireccion = _manejar_error_api(e)
        if redireccion:
            return redireccion

        flash(e.message, "error")
        datos = None

    return render_template(
        "admin/dashboard.html",
        datos=datos,
        seccion="analiticas"
    )


# =========================================================
# CONFIGURACIÓN DEL SISTEMA
# =========================================================

@admin_bp.route("/configuracion", methods=["GET", "POST"])
@admin_required
def configuracion():

    api = _api()

    if request.method == "POST":

        # Los checkbox desmarcados no llegan en el formulario,
        # por eso se reciben los tipos en campos ocultos
        cambios = {}

        for clave in request.form.getlist("claves"):

            tipo = request.form.get(f"tipo_{clave}")

            if tipo == "booleano":
                cambios[clave] = request.form.get(clave) == "on"
            else:
                cambios[clave] = request.form.get(clave, "")

        try:
            api.put("/configuracion", cambios)
            limpiar_cache_tienda()
            flash("Configuración guardada correctamente.", "success")

        except APIErrorAdmin as e:
            redireccion = _manejar_error_api(e)
            if redireccion:
                return redireccion
            flash(e.message, "error")

        return redirect(url_for("admin.configuracion"))

    campos, usuarios = [], []

    try:
        campos = api.get("/configuracion").get("configuracion", [])
        usuarios = api.get("/admin/usuarios")

    except APIErrorAdmin as e:
        redireccion = _manejar_error_api(e)
        if redireccion:
            return redireccion
        flash(e.message, "error")

    return render_template(
        "admin/configuracion.html",
        campos=campos,
        usuarios=usuarios,
        seccion="configuracion"
    )


@admin_bp.route("/usuarios/<int:id_usuario>/rol", methods=["POST"])
@admin_required
def cambiar_rol(id_usuario):

    rol = request.form.get("rol")

    try:
        respuesta = _api().put(f"/admin/usuarios/{id_usuario}/rol", {"rol": rol})
        flash(respuesta.get("message", "Rol actualizado."), "success")

    except APIErrorAdmin as e:
        redireccion = _manejar_error_api(e)
        if redireccion:
            return redireccion
        flash(e.message, "error")

    return redirect(url_for("admin.configuracion") + "#usuarios")
