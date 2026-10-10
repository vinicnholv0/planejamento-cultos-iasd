import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, "database", "culto.db")

SECRET_KEY = "planejamento_cultos_iasd_2026"