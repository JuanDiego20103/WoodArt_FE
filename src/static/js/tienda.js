// =========================================================
// WOODART - FUNCIONES GENERALES DE LA TIENDA
// =========================================================

// ---------- Menú en celulares ----------
document.addEventListener("DOMContentLoaded", () => {

    const boton = document.querySelector(".menu-toggle");
    const menu = document.getElementById("menu-principal");

    if (boton && menu) {
        boton.addEventListener("click", () => {
            const abierto = menu.classList.toggle("active");
            boton.setAttribute("aria-expanded", abierto ? "true" : "false");
        });
    }
});


// ---------- Aviso flotante ----------
let temporizadorToast = null;

function mostrarAviso(mensaje, tipo = "exito", enlace = null) {

    const toast = document.getElementById("toast");

    if (!toast) {
        alert(mensaje);
        return;
    }

    toast.className = "toast " + tipo;
    toast.textContent = mensaje;

    if (enlace) {
        const a = document.createElement("a");
        a.href = enlace.href;
        a.textContent = enlace.texto;
        toast.appendChild(a);
    }

    // Forzar el reinicio de la animación
    void toast.offsetWidth;
    toast.classList.add("visible");

    clearTimeout(temporizadorToast);
    temporizadorToast = setTimeout(() => toast.classList.remove("visible"), 3500);
}


// ---------- Imagen de respaldo si una foto no carga ----------
function imagenNoDisponible(img) {
    const contenedor = img.parentElement;
    img.remove();

    if (contenedor && !contenedor.querySelector(".sin-foto")) {
        const icono = document.createElement("ion-icon");
        icono.setAttribute("name", "image-outline");
        icono.className = "sin-foto";
        contenedor.appendChild(icono);
    }
}


// ---------- Agregar al carrito ----------
async function agregarAlCarrito(idProducto, boton) {

    if (boton) boton.disabled = true;

    try {

        const respuesta = await fetch("/carrito/agregar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_producto: idProducto, cantidad: 1 })
        });

        const data = await respuesta.json().catch(() => ({}));

        if (respuesta.status === 401) {
            mostrarAviso(
                data.error || "Debes iniciar sesión para agregar productos.",
                "error",
                { href: "/login", texto: "Iniciar sesión" }
            );
            return;
        }

        if (!respuesta.ok) {
            mostrarAviso(data.error || "No se pudo agregar el producto al carrito.", "error");
            return;
        }

        mostrarAviso("Producto agregado al carrito.", "exito", { href: "/carrito/", texto: "Ver carrito" });

    } catch (error) {

        console.error("Error:", error);
        mostrarAviso("No se pudo conectar con el servidor.", "error");

    } finally {

        if (boton) boton.disabled = false;
    }
}


// ---------- Buscador con sugerencias ----------
document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.querySelector(".buscador");
    const campo = formulario ? formulario.querySelector("input[name=q]") : null;
    const lista = document.getElementById("sugerencias");

    if (!formulario || !campo || !lista) return;

    let temporizador = null;
    let ultimaBusqueda = "";
    let indiceActivo = -1;

    const formatoPrecio = (valor) =>
        "$" + Math.round(Number(valor) || 0).toLocaleString("es-CO");

    const escapar = (texto) =>
        String(texto ?? "").replace(/[&<>"']/g, (c) => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
        }[c]));

    // Resalta en el nombre las palabras buscadas
    const resaltar = (texto, busqueda) => {
        let html = escapar(texto);
        busqueda.split(/\s+/).filter(Boolean).forEach((palabra) => {
            const seguro = escapar(palabra).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
            html = html.replace(new RegExp(`(${seguro})`, "gi"), "<mark>$1</mark>");
        });
        return html;
    };

    const urlBusqueda = (texto) => `${formulario.action}?q=${encodeURIComponent(texto)}`;

    const cerrar = () => {
        lista.hidden = true;
        lista.innerHTML = "";
        indiceActivo = -1;
        campo.setAttribute("aria-expanded", "false");
    };

    const opciones = () => lista.querySelectorAll("a");

    const marcar = (indice) => {
        const items = opciones();
        items.forEach((el) => el.classList.remove("activa"));
        if (indice >= 0 && indice < items.length) {
            items[indice].classList.add("activa");
            indiceActivo = indice;
        } else {
            indiceActivo = -1;
        }
    };

    const mostrar = (busqueda, datos) => {

        const productos = datos.productos || [];

        if (!productos.length) {
            lista.innerHTML = `<div class="sugerencias-vacio">No encontramos productos para “${escapar(busqueda)}”.</div>`;
        } else {
            lista.innerHTML = productos.map((p) => `
                <a class="sugerencia" role="option" href="${urlBusqueda(p.nombre)}">
                    <span class="sugerencia-imagen">
                        ${p.imagen_principal
                            ? `<img src="${escapar(p.imagen_principal)}" alt="" onerror="this.remove()">`
                            : `<ion-icon name="image-outline"></ion-icon>`}
                    </span>
                    <span class="sugerencia-texto">
                        <strong>${resaltar(p.nombre, busqueda)}</strong>
                        <span>${formatoPrecio(p.precio)}</span>
                    </span>
                </a>`).join("") + `
                <a class="sugerencias-pie" href="${urlBusqueda(busqueda)}">
                    Ver ${datos.total > productos.length ? `los ${datos.total} resultados` : "todos los resultados"} →
                </a>`;
        }

        lista.hidden = false;
        indiceActivo = -1;
        campo.setAttribute("aria-expanded", "true");
    };

    const buscar = async (texto) => {

        try {
            const respuesta = await fetch(`/productos/sugerencias?q=${encodeURIComponent(texto)}`);
            const datos = await respuesta.json();

            // Ignorar respuestas viejas si el usuario siguió escribiendo
            if (texto !== campo.value.trim()) return;

            mostrar(texto, datos);

        } catch (error) {
            cerrar();
        }
    };

    campo.addEventListener("input", () => {

        const texto = campo.value.trim();
        clearTimeout(temporizador);

        if (texto.length < 2) {
            ultimaBusqueda = "";
            cerrar();
            return;
        }

        if (texto === ultimaBusqueda) return;

        temporizador = setTimeout(() => {
            ultimaBusqueda = texto;
            buscar(texto);
        }, 250);
    });

    // Navegar con el teclado: flechas, Enter y Escape
    campo.addEventListener("keydown", (evento) => {

        if (lista.hidden) return;

        const total = opciones().length;

        if (evento.key === "ArrowDown") {
            evento.preventDefault();
            marcar(indiceActivo + 1 >= total ? 0 : indiceActivo + 1);
        } else if (evento.key === "ArrowUp") {
            evento.preventDefault();
            marcar(indiceActivo - 1 < 0 ? total - 1 : indiceActivo - 1);
        } else if (evento.key === "Enter" && indiceActivo >= 0) {
            evento.preventDefault();
            window.location.href = opciones()[indiceActivo].href;
        } else if (evento.key === "Escape") {
            cerrar();
        }
    });

    // No buscar si el campo está vacío
    formulario.addEventListener("submit", (evento) => {
        if (!campo.value.trim()) {
            evento.preventDefault();
            campo.focus();
        }
    });

    // Cerrar al hacer clic fuera
    document.addEventListener("click", (evento) => {
        if (!formulario.contains(evento.target)) cerrar();
    });

    campo.addEventListener("focus", () => {
        if (campo.value.trim().length >= 2 && lista.innerHTML) {
            lista.hidden = false;
        }
    });
});
