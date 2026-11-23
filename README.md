# MADIKEN PERÚ · Smart Furniture Marketplace

Plataforma e-commerce full-stack para muebles a medida: **backend Python con SQLite real, API REST, panel administrativo, MADIKEN IA, pedidos y cotizaciones por WhatsApp y pagos por Yape, Plin o transferencia con verificación manual**.

> Catálogo inicial: se importaron **13 modelos reales del sitio anterior** como ejemplos editables. Las **fotos y los precios son de referencia/demostración** (5 fotos por modelo, tomadas como muestra del tipo de mueble y precios orientativos de tiendas peruanas). **Reemplázalos por tus fotos y precios reales** desde el panel. Puedes borrar los ejemplos con `python run.py limpiar` y empezar vacío. Todo lo que ve el cliente sale de la base de datos que tú administras.
>
> Las **referencias de clientes y las 5 estrellas** son ejemplos marcados como DEMO hasta que las reemplaces por testimonios reales en **Panel → ★ Referencias**.
>
> **Importante:** los controles para cambiar fotos, títulos, precios y marcar **AGOTADO** existen **solo en `/admin.html`** después de iniciar sesión. La tienda pública no muestra botones de edición.
>
> **Visión 2050:** interfaz holográfica con líneas de luz, barridos sobre tarjetas, halo giratorio en el hero, contador y ofertas iridiscentes, MADIKEN IA con pulso 2050 y panel de control con estética de cabina futurista. Todo respeta el blanco, negro, madera y dorado `#e3bd5a`, y sigue funcionando en celular.

---

## 1. Arquitectura

```text
madiken-platform/
├── server/
│   ├── app.py          # API REST + servidor HTTP + SPA + seguridad
│   ├── db.py           # Esquema SQLite y acceso a datos
│   ├── auth.py         # Contraseñas scrypt y sesiones opacas
│   ├── catalog.py      # Catálogo, filtros y búsqueda sin tildes
│   ├── ai.py           # MADIKEN IA fundamentada en datos reales
│   ├── storage.py      # Imágenes validadas y optimizadas
│   └── setup_admin.py  # Crear/actualizar administrador
├── public/
│   ├── index.html      # Tienda (Amazon-like, responsive)
│   ├── admin.html      # Panel administrativo protegido
│   ├── css/            # styles.css + market.css + admin.css
│   ├── js/             # app.js + admin.js
│   ├── uploads/        # Fotos reales (productos, contenido, comprobantes)
│   └── robots.txt
├── data/madiken.db     # Base de datos SQLite (persistente)
├── tests/smoke_test.py # Prueba automática de todos los módulos
└── ABRIR.bat / iniciar.sh
```

Sin Node.js, sin npm y sin dependencias externas: Python 3.10+ (probado con 3.13).

---

## 2. Puesta en marcha local

```powershell
cd madiken-platform
C:\Users\minios\Python313\python.exe run.py admin
C:\Users\minios\Python313\python.exe run.py
```

Abre <http://127.0.0.1:8000> y el panel en <http://127.0.0.1:8000/admin.html>.

Comandos útiles:

```powershell
C:\Users\minios\Python313\python.exe run.py import      # importar los 13 modelos del sitio anterior
C:\Users\minios\Python313\python.exe run.py demo        # cargar 5 fotos demo + precios de referencia (una sola vez)
C:\Users\minios\Python313\python.exe run.py demo-force  # forzar recarga de fotos/precios demo
C:\Users\minios\Python313\python.exe run.py limpiar     # quitar esos ejemplos y dejar el catálogo vacío
C:\Users\minios\Python313\python.exe run.py test        # 54 pruebas automáticas
```

También puedes hacer doble clic en **`ABRIR.bat`**.

El asistente `setup_admin` pide el correo y la contraseña por consola. La contraseña **nunca** se guarda en texto plano: se almacena como hash `scrypt` con sal aleatoria.

Para crear el administrador sin interfaz interactiva (útil en despliegue) usa una variable de entorno temporal; no la escribas en archivos:

```powershell
$env:MADIKEN_ADMIN_PASSWORD="tu-clave-segura"
C:\Users\minios\Python313\python.exe -c "import os,sys; sys.path.insert(0,'.'); from server import auth, db; db.init_db(); print(auth.create_user('admin@madikenperu.com', os.environ['MADIKEN_ADMIN_PASSWORD'], 'Administrador', '', 'admin'))"
Remove-Item Env:MADIKEN_ADMIN_PASSWORD
```

---

## 3. Funcionalidades reales

### Tienda
- Encabezado fijo con categorías, buscador inteligente, favoritos, carrito, cuenta y WhatsApp.
- Banner dinámico editable, destacados, ofertas, recomendaciones y catálogo con paginación.
- Filtros: categoría, precio, material, medidas, color, estilo, disponibilidad, personas y ofertas.
- Fichas con hasta **5 fotos**, miniaturas, zoom, medidas exactas, material, acabado, colores, características, tiempo de fabricación y stock.
- Botones funcionales: agregar al carrito, favoritos, comparar (hasta 3), cotizar, consultar por WhatsApp y pagar con Yape.
- Carrito real en SQLite con cantidades, eliminar, observaciones, subtotal y total.
- Seguimiento de pedido por código + teléfono con los 9 estados.
- Área del cliente: pedidos, favoritos y direcciones (registro opcional).

### MADIKEN IA
- Motor local que **solo** responde con datos del catálogo real en SQLite.
- Interpreta frases como «comedor para 6 personas hasta 1500», detecta categoría, medidas, material, color, estilo y presupuesto.
- Compara productos, explica medidas/materiales/acabados y recomienda por presupuesto.
- Si no hay datos suficientes, deriva al WhatsApp **900589626**. Nunca inventa precios ni stock.
- Opcionalmente usa un proveedor externo configurando `AI_API_KEY` **solo en el servidor**; el catálogo se envía como contexto y la respuesta se valida con el snapshot real.
- Recomendaciones **clicables con foto, precio real, stock y botones de cotizar/WhatsApp**; cuando no hay coincidencias, ofrece derivar a un asesor.

### Cotización y WhatsApp
El mensaje generado es exactamente:

```text
Hola, buenas noches. Quiero que me haga una cotización.

Empresa: MADIKEN PERÚ.

Producto: [Nombre].
Medidas: [Medidas].
Cantidad: [Cantidad].
Material: [Material].
Acabado: [Acabado].
Precio publicado: [Precio].

Quisiera recibir información y una cotización. Muchas gracias.
```

Cada cotización se guarda en la tabla `quotes` antes de abrir WhatsApp.

### Medios de pago
- **Yape (activo por defecto):** número **900589626**, nombre comercial **MADIKEN PERÚ**. Botón de copiar, monto editable y envío de comprobante desde el celular.
- **Titular protegido:** el nombre completo **WILFREDO MAURICIO HUAMAN BRAVO** se guarda solo en el panel. En la tienda y en WhatsApp aparece a medias: **WILFREDO M. H. B.** Así el cliente ve tu Yape y tu nombre, sin exponer tus datos completos.
- **Plin y transferencia bancaria:** vienen desactivados; actívalos y llena sus datos cuando quieras en **Panel → ⚙ Configuración y backups**. La tienda pública los mostrará sola, sin controles de edición.
- El comprobante se guarda en `public/uploads/comprobantes` y se registra en `payments` con el medio elegido (`yape`, `plin` o `bank`).
- **El pago jamás se confirma automáticamente**: el administrador verifica el comprobante y el ingreso del dinero.

### Panel administrativo (`/admin.html`)
- Dashboard real: ventas entregadas, pedidos, cotizaciones, clientes, pagos, productos más consultados, búsquedas frecuentes, productos sin foto y descripciones cortas.
- CRUD de productos (hasta 5 fotos optimizadas desde el celular), categorías, ofertas, ocultar/eliminar.
- Subida rápida visible en **Productos → 📷 Subir fotos a mi catálogo**: eliges el modelo, seleccionas varias fotos y guardas.
- En **Categorías → Modelos por categoría** cada tarjeta permite cambiar precio, subir fotos y alternar **Disponible / Agotado** con un toque.
- Pedidos con los 9 estados, adelanto, saldo, pagos Yape y verificación manual.
- **★ Referencias**: alta, edición, ocultar y borrado de testimonios; muestran nombre, ciudad, producto y estrellas. Los ejemplos vienen marcados DEMO y avisan en la tienda hasta que los reemplaces.
- Contenido: logo, banner, novedades, texto, redes; WhatsApp, Yape y ajustes.
- Generador de descripciones comerciales con datos reales del producto.
- Respaldo y restauración JSON.

---

## 4. API REST

| Método | Ruta | Uso |
|---|---|---|
| GET | `/api/bootstrap` | Ajustes, categorías, contenido y usuario |
| GET | `/api/products?...` | Catálogo con filtros y paginación |
| GET | `/api/products/{id}` | Ficha + relacionados |
| GET | `/api/ai/interpret?q=` | Búsqueda en lenguaje natural |
| POST | `/api/ai/chat` | MADIKEN IA |
| GET | `/api/testimonials` | Referencias publicadas y promedio de estrellas |
| GET/POST/PATCH/DELETE | `/api/admin/testimonials` | Gestión de referencias (admin) |
| GET/POST | `/api/cart`, `/api/cart/add`, `/api/cart/update`, `/api/cart/remove`, `/api/cart/clear` | Carrito |
| POST | `/api/quotes` | Cotización + link de WhatsApp |
| POST | `/api/orders` | Pedido + link de WhatsApp |
| GET | `/api/orders/track?code=&phone=` | Seguimiento |
| POST | `/api/yape/receipt` | Registro de comprobante |
| POST | `/api/auth/login`, `/register`, `/logout` | Autenticación |
| GET | `/api/account/me`, `/orders`, `/favorites`, `/addresses` | Área del cliente |
| GET/POST/PATCH/DELETE | `/api/admin/*` | Panel protegido (rol admin) |
| POST | `/api/admin/products/{id}/stock` | Alternar Disponible / Agotado |
| GET | `/api/health` | Diagnóstico |
| GET | `/sitemap.xml` | Sitemap dinámico |

Todas las escrituras exigen la cabecera `X-Requested-With: MadikenApp`, validan `Origin`, aplican límite de velocidad y usan cookies `HttpOnly`, `SameSite=Lax`.

---

## 5. Seguridad

- Contraseñas `scrypt` con sal aleatoria; sesiones opacas en SQLite con expiración de 7 días.
- Acceso al panel solo con rol `admin` (verificado en cada petición).
- Imágenes: se valida el tipo MIME declarado **y** la firma binaria; máximo 8 MB por archivo y **5 fotos por producto** (en alta rápida y en edición). Si el modelo ya tiene 5, marca **«Reemplazar fotos actuales»** para cambiarlas.
- Rutas de archivos restringidas al directorio `public`.
- Sin credenciales ni claves API en el frontend ni en el repositorio.
- `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` y `Cache-Control: no-store` en API.
- En producción, HTTPS + `COOKIE_SECURE=1`.

---

## 6. Pruebas

```powershell
C:\Users\minios\Python313\python.exe run.py test
```

La prueba crea una base temporal, un administrador, productos, un carrito, una cotización, un pedido, un comprobante Yape y consulta el dashboard, IA y sitemap. No toca tu base real.

---

## 7. Despliegue

- **Todo en un solo servicio (recomendado):** proveedor con Python + **disco persistente** para `data/` y `public/uploads/`, HTTPS y variable `MADIKEN_BASE_URL`. Ver `COMO_ACTUALIZAR.md`.
- **Netlify con un solo archivo:** arrastra `netlify-public.zip` a Netlify Drop. La tienda funciona en modo catálogo autónomo con los datos exportados en `public/js/standalone-data.js` (categorías, fotos, precios, ofertas, carrito, cotizaciones y pagos). El panel y los pedidos reales requieren la API.
- **Netlify + API externa:** la tienda estática se publica en Netlify y la lógica corre en Render u otro host Python. Netlify hace de proxy de `/api/*` y `/uploads/*`, así que no hay problemas de CORS ni de cookies. Ver **`DEPLOY_NETLIFY.md`** y el archivo `public/_redirects`. Si editas el catálogo, ejecuta `python run.py export_standalone` y vuelve a subir `public/`.
