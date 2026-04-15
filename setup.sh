#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
REQ_FILE="requirements.txt"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is not installed or not on PATH."
  exit 1
fi

if [[ ! -f "$REQ_FILE" ]]; then
  echo "Error: $REQ_FILE not found in $(pwd)"
  exit 1
fi

echo "Creating virtual environment in $VENV_DIR ..."
python3 -m venv "$VENV_DIR"

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Upgrading pip/setuptools/wheel ..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing dependencies from $REQ_FILE ..."
pip install -r "$REQ_FILE"

echo "Verifying required imports ..."
python - <<'PY'
import importlib

modules = [
    "dotenv",
    "ddgs",
    "google.genai",
]

missing = []
for module in modules:
    try:
        importlib.import_module(module)
    except Exception:
        missing.append(module)

if missing:
    raise SystemExit(f"Missing modules after install: {missing}")

try:
    import tkinter  # noqa: F401
except Exception:
    print("Warning: tkinter is not available. Install your OS package (e.g. python3-tk).")

print("Environment setup verification complete.")
PY

echo
echo "Setup complete. Activate with: source $VENV_DIR/bin/activate"
echo "Run app from repo root with: python main/main.py"
