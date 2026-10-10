import sqlite3

banco = sqlite3.connect("database/culto.db")
cursor = banco.cursor()

# ==========================
# ESCALAS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS escalas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    mes INTEGER NOT NULL,

    ano INTEGER NOT NULL,

    observacoes TEXT

)
""")


# ==========================
# ITENS DA ESCALA
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS escala_itens (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    escala_id INTEGER NOT NULL,

    data TEXT NOT NULL,

    participante_id INTEGER,

    funcao_id INTEGER,

    observacao TEXT,

    ordem INTEGER,

    FOREIGN KEY (escala_id)
        REFERENCES escalas(id),

    FOREIGN KEY (participante_id)
        REFERENCES participantes(id),

    FOREIGN KEY (funcao_id)
        REFERENCES funcoes(id)

)
""")


banco.commit()
banco.close()

print("Banco de escalas criado com sucesso!")