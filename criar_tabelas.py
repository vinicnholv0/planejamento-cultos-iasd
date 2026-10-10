import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB = os.path.join(BASE_DIR, "culto.db")

conexao = sqlite3.connect(DB)
cursor = conexao.cursor()

# ==========================
# PARTICIPANTES
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS participantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    observacoes TEXT,
    status TEXT DEFAULT 'Ativo'
)
""")

# ==========================
# FUNÇÕES
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS funcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
)
""")

# ==========================
# PARTICIPANTE x FUNÇÕES
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS participante_funcoes (
    participante_id INTEGER,
    funcao_id INTEGER,
    PRIMARY KEY (participante_id, funcao_id),
    FOREIGN KEY (participante_id) REFERENCES participantes(id),
    FOREIGN KEY (funcao_id) REFERENCES funcoes(id)
)
""")

# ==========================
# CULTOS
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS cultos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    tipo TEXT,
    tema TEXT,
    hino_inicial TEXT,
    hino_final TEXT,
    observacoes TEXT
)
""")

# ==========================
# PARTICIPAÇÕES DO CULTO
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS culto_participantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    culto_id INTEGER,
    participante_id INTEGER,
    funcao_id INTEGER,
    FOREIGN KEY (culto_id) REFERENCES cultos(id),
    FOREIGN KEY (participante_id) REFERENCES participantes(id),
    FOREIGN KEY (funcao_id) REFERENCES funcoes(id)
)
""")

# ==========================
# INSERE FUNÇÕES PADRÃO
# ==========================

funcoes = [
    "Pastor",
    "Ancião",
    "Diretor de Culto",
    "Diácono",
    "Diaconisa",
    "Pianista",
    "Organista",
    "Louvor",
    "Música Especial",
    "Sonoplastia",
    "Mídia",
    "Recepção",
    "Ministério Infantil"
]

for funcao in funcoes:
    cursor.execute(
        "INSERT OR IGNORE INTO funcoes(nome) VALUES(?)",
        (funcao,)
    )
# ==========================
# USUÁRIOS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    nivel TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()

print("Banco criado com sucesso!")