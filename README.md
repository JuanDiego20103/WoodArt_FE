# WoodArt — Frontend (tienda)

Tienda en línea de **WoodArt**, productos en madera: maderas, muebles, herrajes, pisos y puertas. Arma las páginas que ve el usuario y obtiene todos los datos de la API del proyecto **WoodArt_backend**, que debe estar corriendo.

Proyecto del programa **Análisis y Desarrollo de Software (ADSO)** — ficha 3186693.

## Funcionalidades

**Tienda**

- Página de inicio con categorías, productos destacados y banner de ofertas
- Catálogo con paginación (8 productos por página) y una página por categoría
- **Buscador** con sugerencias mientras se escribe y página de resultados
- Registro e inicio de sesión de clientes
- **Carrito**: agregar productos sin recargar la página, ver el total y quitar productos
- Diseño adaptable a celular

**Panel de administración** (`/admin`)

- Inicio de sesión solo para cuentas con rol de administrador
- **Analíticas**: ingresos, pedidos por estado, ventas de los últimos 6 meses, productos más vendidos, stock bajo y últimos pedidos
- **Configuración** de la tienda: nombre, mensaje de ofertas, umbral de stock bajo, registro abierto o cerrado y **modo mantenimiento**
- **Usuarios y roles**: convertir clientes en administradores o quitarles el permiso

## Tecnologías

| Tecnología | Uso |
| --- | --- |
| Python + Flask 3 | Rutas de la tienda y sesión del usuario |
| Jinja2 | Plantillas HTML con herencia y piezas reutilizables |
| httpx | Peticiones HTTP a la API del backend |
| HTML, CSS y JavaScript | Diseño, carrito sin recarga y buscador con sugerencias |
| Ionicons y Google Fonts (Ubuntu) | Íconos y tipografía |

## Requisitos

- Python 3.12 o superior
- El backend **WoodArt_backend** corriendo en `http://127.0.0.1:5000`

## Instalación

```bash
# 1. Crear y activar el entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar las dependencias
pip install flask httpx python-dotenv
```

3. Opcional: crea un archivo `.env` en esta carpeta para cambiar la configuración. Si no existe, se usan los valores por defecto. Este archivo **no se sube al repositorio**.

```env
SECRET_KEY=escribe-aqui-una-clave-para-las-sesiones
API_BASE_URL=http://127.0.0.1:5000/api/v1
```

## Ejecución

Con doble clic en **`iniciar_frontend.bat`**, o desde la carpeta `WoodArt`:

```bash
.venv\Scripts\python.exe -m src.app
```

La tienda queda en **http://localhost:5001** y el panel en **http://localhost:5001/admin/login**.

Para entrar al panel necesitas una cuenta de administrador. Créala con `crear_admin.bat` en el proyecto del backend.

## Estructura

```
WoodArt/
├── iniciar_frontend.bat
└── src/
    ├── app.py                 # Punto de entrada (puerto 5001)
    ├── __init__.py            # create_app: blueprints, configuración de la tienda y modo mantenimiento
    ├── config/
    │   ├── config.py          # SECRET_KEY y dirección de la API
    │   └── tienda.py          # Configuración pública de la tienda (con caché de 15 s)
    ├── controllers/           # Rutas: inicio, productos, carrito, usuarios y panel admin
    ├── admin/, carrito/, productos/, usuarios/, pedidos/, inventario/
    │                          # Clientes HTTP de la API (envían el token Bearer)
    ├── templates/
    │   ├── layout.html        # Base: encabezado, buscador, mensajes y pie de página
    │   ├── categoria.html     # Base de las páginas de categoría
    │   ├── partials/          # Tarjeta de producto, filtros, paginación y grilla
    │   └── admin/             # Login, analíticas y configuración del panel
    └── static/
        ├── css/               # Estilos de la tienda (layout.css) y de cada página
        ├── js/tienda.js       # Carrito, avisos, buscador con sugerencias y menú móvil
        └── img/               # Logo y favicon
```

## Rutas

| Ruta | Descripción |
| --- | --- |
| `/` | Página de inicio |
| `/productos/` | Catálogo; acepta `?q=` para buscar y `?page=` para paginar |
| `/productos/maderas`, `/muebles`, `/herrajes`, `/pisos`, `/puertas` | Páginas de categoría |
| `/productos/sugerencias?q=` | Sugerencias del buscador (JSON) |
| `/login` | Inicio de sesión y registro de clientes |
| `/carrito/` | Carrito del cliente |
| `/admin/login` | Inicio de sesión del panel |
| `/admin/` | Analíticas |
| `/admin/configuracion` | Configuración de la tienda y roles de usuarios |

## Autor

Juan Diego Bulla Rodríguez — ADSO, ficha 3186693.
