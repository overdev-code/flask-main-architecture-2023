import sys
import os

# Agregar la carpeta 'app' al PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app

if __name__ == "__main__":
    app.run()  # No añadir parámetros, modificar directamente en Config
