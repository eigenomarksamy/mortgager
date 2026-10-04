"""Builds a static version of mortgager in dist/ that needs no server.

It is the same page the Flask app serves (templates/index.html and static/),
plus the Python sources from src/. A config snippet injected into the page
makes static/js/script.js run src/api.py in the browser with Pyodide instead
of posting to Flask's /calculate endpoint.

Usage:
    python3 build_static.py
    python3 -m http.server -d dist    # then open http://localhost:8000
"""
import json
import shutil
from pathlib import Path

PYODIDE_VERSION = '314.0.7'

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
SCRIPT_TAG = '<script src="static/js/script.js"'


def main() -> None:
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(ROOT / 'static', DIST / 'static')

    python_files = sorted(path.name for path in (ROOT / 'src').glob('*.py'))
    (DIST / 'src').mkdir(parents=True)
    for name in python_files:
        shutil.copy2(ROOT / 'src' / name, DIST / 'src' / name)

    html = (ROOT / 'templates' / 'index.html').read_text(encoding='utf-8')
    if SCRIPT_TAG not in html:
        raise SystemExit(f'build_static.py: could not find {SCRIPT_TAG!r} in templates/index.html')
    config = json.dumps({'backend': 'browser', 'pythonFiles': python_files})
    injected = (
        f'<script>window.MORTGAGER = {config};</script>\n'
        f'    <script src="https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js" defer></script>\n'
        f'    {SCRIPT_TAG}'
    )
    (DIST / 'index.html').write_text(html.replace(SCRIPT_TAG, injected, 1), encoding='utf-8')

    print(f'Built dist/ with {len(python_files)} Python files: {", ".join(python_files)}')


if __name__ == '__main__':
    main()
