
import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CAMINHO_BANCO = os.path.join(BASE_DIR, "database", "culto.db")

banco = sqlite3.connect(CAMINHO_BANCO)
cursor = banco.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    nivel TEXT NOT NULL
)
""")

banco.commit()
banco.close()

print("Tabela de usuários verificada com sucesso.")
print("Crie os usuários pelo sistema com senhas seguras.")
