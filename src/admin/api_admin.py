import httpx
from flask import current_app


class APIErrorAdmin(Exception):
    def __init__(self, message, status_code=400, errors=None):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)


class APIAdmin:
    """Cliente del backend para el panel de administración."""

    def __init__(self, token: str = None):
        self.base_url = current_app.config['API_BASE_URL']
        self.headers = {'Content-Type': 'application/json'}
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _handle(self, response: httpx.Response):
        if not response.content:
            raise APIErrorAdmin('El servidor retornó una respuesta vacía', response.status_code)

        try:
            body = response.json()
        except Exception:
            raise APIErrorAdmin(
                f'Respuesta no es JSON válido (status {response.status_code})',
                response.status_code
            )

        if response.status_code < 400:
            return body

        mensaje = 'Error del servidor'
        if isinstance(body, dict):
            mensaje = body.get('message') or body.get('error') or mensaje

        raise APIErrorAdmin(mensaje, response.status_code)

    def _request(self, metodo, path, **kwargs):
        try:
            r = httpx.request(metodo, self._url(path), headers=self.headers, timeout=10, **kwargs)
        except httpx.HTTPError:
            raise APIErrorAdmin('No se pudo conectar con el backend. ¿Está corriendo?', 503)
        return self._handle(r)

    def get(self, path, params=None):
        return self._request('GET', path, params=params)

    def post(self, path, data=None):
        return self._request('POST', path, json=data)

    def put(self, path, data=None):
        return self._request('PUT', path, json=data)
