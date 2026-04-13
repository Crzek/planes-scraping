# config.py

import sys
import os

# Ruta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Agrega la ruta al directorio raíz al sys.path
sys.path.append(BASE_DIR)

# DB
DATABASE_URL = 'postgresql://user:pass@host:5432/database'
DEBUG = True
SECRET_KEY = 'mysecretkey'
