from flask import Flask, session


def create_app(config_name='default'):
    app = Flask(__name__)
    from src.config.config import config
    app.config.from_object(config[config_name])

    from src.controllers.usuarios_controller import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
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

    return app