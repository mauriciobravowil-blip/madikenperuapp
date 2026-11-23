"""Lanzador de MADIKEN PERÚ.

Uso:
  python run.py          → iniciar servidor
  python run.py admin    → crear/actualizar administrador
  python run.py import   → importar modelos del sitio anterior como ejemplos
  python run.py limpiar  → quitar esos ejemplos editables
  python run.py demo     → cargar 5 fotos y precios de referencia (una sola vez)
  python run.py demo-force → volver a aplicar fotos/precios demo
  python run.py test     → prueba integral con base temporal
  python run.py export_standalone → exportar catálogo para Netlify (un archivo)
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else "server"
    if command == "admin":
        from server import setup_admin
        setup_admin.main()
    elif command == "test":
        from tests import smoke_test
        smoke_test.main()
    elif command == "init":
        from server import db
        db.init_db()
        print("Base de datos inicializada:", db.DB_PATH)
    elif command == "import":
        from server import import_legacy
        import_legacy.main()
    elif command == "limpiar":
        from server import import_legacy
        import_legacy.clear()
    elif command == "demo":
        from server import import_demo_photos
        import_demo_photos.main(force=False)
    elif command == "demo-force":
        from server import import_demo_photos
        import_demo_photos.main(force=True)
    elif command == "export_standalone":
        from server import export_standalone
        export_standalone.main()
    elif command == "server":
        from server import app
        app.main()
    else:
        raise SystemExit(f"Comando desconocido: {command}")


if __name__ == "__main__":
    main()
