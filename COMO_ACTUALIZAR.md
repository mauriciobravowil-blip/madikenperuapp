# Cómo actualizar y publicar MADIKEN PERÚ

Esta carpeta es la plataforma real (Python + SQLite). **No la subas a Netlify Drop**: ese servicio solo publica archivos estáticos y no puede ejecutar el backend ni conservar la base de datos.

## 1. Trabajar en local

```powershell
cd madiken-platform
C:\Users\minios\Python313\python.exe run.py
```

- Tienda: <http://127.0.0.1:8000>
- Panel privado: <http://127.0.0.1:8000/admin.html>

Inicia sesión con el correo y la contraseña del administrador. **Solo en el panel** puedes cambiar fotos, títulos, precios, medidas y marcar modelos como **AGOTADO**. Los clientes no ven esos controles.

> **Antes de publicar:** las fotos y los precios actuales son **de referencia/demostración**. Reemplázalos por tus fotos y precios reales. Las referencias de clientes también son ejemplos marcados DEMO; cámbialas en **★ Referencias**.

## 2. Fotos del catálogo (máximo 5 por modelo)

En el panel, entra a **Productos** y usa el bloque visible:

**📷 Subir fotos a mi catálogo**

1. Elige el modelo.
2. Selecciona varias fotos a la vez (hasta 5 por modelo).
3. Si el modelo **ya tiene 5 fotos**, marca **«Reemplazar fotos actuales»** para sustituir las de demostración por las tuyas.
4. Pulsa **Guardar fotos en el modelo**.

También puedes entrar a **Categorías → Modelos por categoría**: cada tarjeta tiene **📷 Subir fotos**, edición rápida de precio y el botón **Disponible / Agotado**.

Las imágenes se optimizan solas, se validan y se guardan en `public/uploads/productos/`.

## 2b. Referencias y estrellas

En **★ Referencias** puedes agregar testimonios reales con nombre, ciudad, producto, mensaje y de 1 a 5 estrellas. La tienda calcula el promedio y muestra las estrellas en el inicio y en la sección «Lo que dicen nuestros clientes». Mientras queden ejemplos, aparece un aviso de demostración.

## 3. Modelos importados del sitio anterior

Se importaron 13 modelos reales del sitio estático anterior con sus precios y stock. Son **ejemplos editables**. Las fotos (5 por modelo) y los precios actuales son **de referencia/demostración** y deben reemplazarse por los reales antes de publicar.

```powershell
C:\Users\minios\Python313\python.exe run.py import      # importar si faltan
C:\Users\minios\Python313\python.exe run.py demo        # fotos/precios demo (una sola vez)
C:\Users\minios\Python313\python.exe run.py demo-force  # forzar recarga demo
C:\Users\minios\Python313\python.exe run.py limpiar     # dejar el catálogo vacío
```

## 4. Publicación (hosting)

Necesitas un proveedor con **Python + disco persistente + HTTPS**. Ejemplos: VPS con Python, Render/Railway/Fly.io con volumen persistente, o un servidor propio con Nginx + HTTPS.

Variables de entorno en el servidor (nunca en el frontend):

```bash
MADIKEN_BASE_URL=https://tu-dominio.com
COOKIE_SECURE=1
MADIKEN_DB=/ruta/persistente/madiken.db
# AI_API_KEY=...   (opcional; solo si contratas un proveedor de IA)
```

Puntos críticos:

1. Sirve `public/` como carpeta web y ejecuta `python run.py` como servicio.
2. Persiste `data/` y `public/uploads/` entre despliegues; ahí están la base y las fotos.
3. Usa HTTPS y `COOKIE_SECURE=1` para que las cookies de sesión funcionen de forma segura.
4. Crea el administrador con `run.py admin` o con `MADIKEN_ADMIN_PASSWORD` temporal en el servidor; no escribas la clave en archivos del proyecto.
5. Configura `MADIKEN_BASE_URL` con tu dominio para los enlaces de WhatsApp, Yape y sitemap.

## 5. Actualizar una versión ya instalada

1. Copia los archivos nuevos (`server/`, `public/`, `run.py`, `README.md`).
2. **No reemplaces** `data/madiken.db` ni `public/uploads/` si ya tienes pedidos o fotos reales.
3. Ejecuta las pruebas:

```powershell
$env:PYTHONIOENCODING="utf-8"
C:\Users\minios\Python313\python.exe run.py test
```

4. Reinicia el servicio Python.

## 6. Copias de seguridad

En **Configuración y backups** del panel puedes descargar un JSON con la base. Guarda también `public/uploads/` por separado porque las fotos son archivos, no filas SQLite.

## 7. Verificación rápida

```powershell
C:\Users\minios\Python313\python.exe run.py test
```

Debe terminar con `57/57 pruebas correctas`.

## 8. Titular de los pagos

En **Panel → ⚙ Configuración y backups** está tu nombre completo como titular real (`WILFREDO MAURICIO HUAMAN BRAVO`) para Yape, Plin y banco. La tienda pública nunca lo expone completo: muestra **WILFREDO M. H. B.** junto a **MADIKEN PERÚ** y el número **900589626**. No hace falta cambiar nada para que funcione; si algún día cambias de titular, edítalo solo en el panel.
