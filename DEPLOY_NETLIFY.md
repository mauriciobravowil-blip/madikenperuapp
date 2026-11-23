# MADIKEN PERÚ · Netlify en un solo archivo

## Subir la página (lo que pediste)

1. Descarga **`netlify-public.zip`**.
2. Entra a https://app.netlify.com/drop y arrastra **ese ZIP** (o solo la carpeta `public/`).
3. Netlify te da una URL, por ejemplo `https://madiken-peru-abc123.netlify.app`.
4. Listo: la tienda se abre con categorías, fotos, precios, ofertas, carrito, cotizaciones por WhatsApp y datos de pago.

No hay que configurar variables, dominios ni servidores. **No subas `madiken-platform.zip` a Netlify**: ese es el código Python de la API y Netlify no lo ejecuta.

### Qué funciona en este modo
- Catálogo completo: 13 modelos, 7 categorías, 65 fotos y precios de referencia.
- Ofertas 2050, contador, testimonios, novedades y búsqueda/IA local sobre productos reales.
- Carrito, comparador, favoritos y cotizaciones con el texto exacto para WhatsApp.
- Carrito y pedidos se guardan **en tu navegador** (no en la nube).

### Qué NO funciona sin la API
- Panel administrativo (`/admin.html`): verás un aviso indicando que necesita la API.
- Pedidos reales, stock compartido, historial en la nube, subida de fotos, cambios de precio y verificación de pagos.

Cuando quieras el sistema completo, publica la API Python en Render/Fly/PythonAnywhere y activa el proxy de `/api/*` en `public/_redirects` (instrucciones al final de `render.yaml` y de este documento).

---

## Modo completo opcional (Netlify + API externa)

1. Sube `madiken-platform/` a GitHub y crea el servicio en Render con `render.yaml` (plan `starter`, disco persistente `/data`). Cambia `TU-SITIO.netlify.app` por tu URL de Netlify.
2. Copia la URL de la API, por ejemplo `https://madiken-api.onrender.com`.
3. En `public/_redirects`, descomenta y completa:

```
/api/*      https://TU-API.onrender.com/api/:splat     200!
/uploads/*  https://TU-API.onrender.com/uploads/:splat 200!
```

4. Vuelve a subir `public/` a Netlify.
5. En Render ajusta `MADIKEN_BASE_URL` y `MADIKEN_FRONTEND_URL` a tu URL de Netlify y redespliega.

El frontend detectaautomáticamente si la API responde: si responde, usa datos reales; si no, usa el catálogo exportado. Por eso el mismo ZIP sirve para los dos casos.

---

## Actualizar los datos exportados

Si editas productos en la API y quieres reflejarlos en la versión estática:

```powershell
cd madiken-platform
python run.py export_standalone
```

Eso regenera `public/js/standalone-data.js`. Luego vuelve a comprimir `public/` y súbelo a Netlify.
