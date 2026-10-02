#!/usr/bin/env python3
"""Empaqueta la skill en archivos zip para subirla (por ejemplo, en claude.ai → Settings → Capabilities → Skills).

  python tools/package_skill.py          # dist/marca.zip (completa) + dist/marca-lite.zip

El paquete lite deja fuera los más de 1400 archivos SVG y gallery.html (conserva los metadatos del catálogo,
los scripts y todas las referencias) para plataformas con límite de tamaño de subida.
"""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "marca")
DIST = os.path.join(ROOT, "dist")
SKIP_DIRS = {"__pycache__", ".DS_Store"}


def build(name, lite):
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, name)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(SKILL):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            rel_dir = os.path.relpath(dirpath, SKILL)
            if lite and rel_dir.replace(os.sep, "/").startswith("assets/library/svg"):
                continue
            for fn in filenames:
                if fn in SKIP_DIRS or fn.endswith(".pyc"):
                    continue
                if lite and fn == "gallery.html":
                    continue
                full = os.path.join(dirpath, fn)
                z.write(full, os.path.join("marca", os.path.relpath(full, SKILL)))
    print(f"{out}  {os.path.getsize(out) / 1e6:.1f} MB")


if __name__ == "__main__":
    build("marca.zip", lite=False)
    build("marca-lite.zip", lite=True)
