# Activar la API de MADIKEN PERÚ (panel administrativo)

La webpage ya está en Netlify. Ahora activamos el "cerebro": la API Python. El proveedor recomendado es **Render** porque lee el archivo `render.yaml` automáticamente.

---

## Paso 1 — Crear el repositorio en GitHub

1. Entra a https://github.com/new
2. Nombre del repo: `madiken-api` (o el que quieras)
3. Déjalo **Public** o **Private** (los dos funcionan)
4. No marques nada más. Crea el repositorio.
5. Descomprime `madiken-platform.zip` en tu PC.
6. Entra a la carpeta que sale (`madiken-platform`).
7. En la página del repo, haz clic en **Add file → Upload files**.
8. Arrastra **todo lo que hay dentro de esa carpeta** (`run.py`, `render.yaml`, `server/`, `public/`, `tests/`, `data/`, `README.md`, etc.).
   - Ojo: sube el **contenido**, no la carpeta entera dentro de otra.
9. Haz clic en **Commit changes**.

---

## Paso 2 — Crear el servicio en Render

1. Entra a https://render.com y regístrate/inicia sesión (puedes usar tu GitHub).
2. Clic en **New → Blueprint**.
3. Autoriza Render a leer tu GitHub y selecciona el repo `madiken-api`.
4. Render detectará `render.yaml`. Revisa la configuración.
5. Cambia el plan a **Starter** (USD 7/mes aprox.). El plan Free **no tiene disco persistente** y perderías la base de datos y las fotos al reiniciar.
6. Clic en **Apply** / **Deploy**.

---

## Paso 3 — Ajustar las URLs

Cuando Render termine el deploy, verás una URL tipo:

```text
https://madiken-api.onrender.com
```

### 3.1 En Render → tu servicio → Environment

Edita estas dos variables con la URL de tu tienda en Netlify:

```text
MADIKEN_BASE_URL = https://madikenperuapp.netlify.app
MADIKEN_FRONTEND_URL = https://madikenperuapp.netlify.app
```

Guarda y haz **Manual Deploy → Deploy latest commit**.

### 3.2 Probar la API

Abre:

```text
https://madiken-api.onrender.com/health
```

Debe responder algo como:

```json
{"ok": true, "service": "madiken-platform", "db": "madiken.db"}
```

---

## Paso 4 — Conectar Netlify con la API

1. En tu repo de GitHub, abre `public/_redirects`.
2. Deja el archivo así (cambia la URL por la real de Render):

```text
/api/*      https://madiken-api.onrender.com/api/:splat     200!
/uploads/*  https://madiken-api.onrender.com/uploads/:splat 200!

/*  /index.html  200
```

3. Haz **Commit changes**. Netlify detectará el cambio si el sitio está conectado al repo.
   - Si tu sitio de Netlify se creó con Drop (no conectado a GitHub), entonces edita `public/_redirects` en tu PC, vuelve a generar el ZIP con `python build_netlify_zip.py` y súbelo de nuevo a Netlify.

---

## Paso 5 — Probar el panel

Abre:

```text
https://madikenperuapp.netlify.app/admin.html
```

Ingresa con:

```text
Correo:     admin@madikenperu.com
Contraseña: Madiken2050-TOW9ND
```

Si entra, la API está activa ✅

Después cambia la clave en cuanto puedas. En Render entra a tu servicio → pestaña **Shell** y ejecuta:

```bash
python run.py admin
```

El asistente te pedirá el correo y la nueva contraseña. Eso actualiza la base que está en el disco persistente `/data/madiken.db`. Reinicia el servicio desde Render para que tome el cambio.

---

## Qué conservar

En Render el disco persistente `/data` guarda:

```text
/data/madiken.db
/data/uploads
```

El primer arranque copia automáticamente la base y las fotos incluidas en el repo. No borres ese disco.

---

## Si Render tarda en responder

El plan Starter no duerme. Si usas el plan Free, el primer request después de un rato puede tardar ~30 segundos mientras el servicio despierta. Por eso se recomienda Starter.
