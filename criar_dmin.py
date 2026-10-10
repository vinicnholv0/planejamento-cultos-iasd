
import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CAMINHO_BANCO = os.path.join(BASE_DIR, "database", "culto.db")

banco = sqlite3.connect(CAMINHO_BANCO)
cursor = banco.cursor()

print("Este script não cria usuários automaticamente.")
print("Cadastre usuários pelo sistema, usando uma senha segura.")

banco.close()
