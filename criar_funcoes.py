import sqlite3

banco = sqlite3.connect("database/culto.db")
cursor = banco.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcoes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL UNIQUE,

    descricao TEXT

)
""")

banco.commit()
banco.close()

print("Tabela de funções criada com sucesso!")