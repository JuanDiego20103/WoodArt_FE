from flask import Flask, session, request, render_template


def create_app(config_name='default'):
    app = Flask(__name__)
    from src.config.config import config
    app.config.from_object(config[config_name])

    from src.controllers.usuarios_controller import usuarios_bp
    app.register_blueprint(usuarios_bp,)
    from src.controllers.productos_controller import productos_bp
    app.register_blueprint(productos_bp, url_prefix='/productos')
    from src.controllers.carrito_controller import carrito_bp
    app.register_blueprint(carrito_bp, url_prefix='/carrito')
    from src.controllers.pedidos_controller import pedidos_bp
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    from src.controllers.inventario_controller import inventario_bp
    app.register_blueprint(inventario_bp, url_prefix='/inventario')
    from src.controllers.home_controller import home_bp
    app.register_blueprint(home_bp, url_prefix='/')
    from src.controllers.admin_controller import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from src.config.tienda import obtener_config_tienda

    # La configuración de la tienda queda disponible en todas las plantillas
    @app.context_processor
    def inyectar_config_tienda():
        from datetime import date
        return {"tienda": obtener_config_tienda(), "anio_actual": date.today().year}

    # Modo mantenimiento: los clientes ven un aviso, los administradores no
    @app.before_request
    def verificar_mantenimiento():

        if request.endpoint is None or request.endpoint == "static":
            return None

        if request.blueprint == "admin":
            return None

        if request.endpoint in ("usuarios.mostrar_login", "usuarios.login", "usuarios.logout"):
            return None

        usuario = session.get("usuario")
        if usuario and usuario.get("rol") == "admin":
            return None

        if obtener_config_tienda().get("modo_mantenimiento"):
            return render_template("mantenimiento.html"), 503

        return None

    return app