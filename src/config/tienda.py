import time

import httpx
from flask import current_app

# Valores que se usan si el backend no responde
CONFIG_TIENDA_DEFECTO = {
    "nombre_tienda": "WoodArt",
    "mensaje_oferta": "🔥 20% de descuento en muebles seleccionados",
    "registro_abierto": True,
    "modo_mantenimiento": False,
    "mensaje_mantenimiento": "Estamos haciendo mejoras en la tienda. Vuelve pronto."
}

# Se guarda unos segundos en memoria para no consultar el backend en cada página
_SEGUNDOS_CACHE = 15
_cache = {"datos": None, "hora": 0}


def obtener_config_tienda():

    if _cache["datos"] and time.time() - _cache["hora"] < _SEGUNDOS_CACHE:
        return _cache["datos"]

    datos = dict(CONFIG_TIENDA_DEFECTO)

    try:
        url = f"{current_app.config['API_BASE_URL'].rstrip('/')}/configuracion/publica"
        r = httpx.get(url, timeout=3)
        if r.status_code == 200:
            datos.update(r.json())
    except (httpx.HTTPError, ValueError):
        pass

    _cache["datos"] = datos
    _cache["hora"] = time.time()

    return datos


def limpiar_cache_tienda():
    _cache["datos"] = None
