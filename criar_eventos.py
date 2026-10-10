import sqlite3

banco = sqlite3.connect("database/culto.db")
cursor = banco.cursor()

# ===========================================
# TABELA DE EVENTOS
# ===========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    tipo TEXT NOT NULL,

    data_inicio TEXT NOT NULL,

    hora_inicio TEXT NOT NULL,

    data_fim TEXT,

    hora_fim TEXT,

    local TEXT,

    responsavel INTEGER,

    descricao TEXT,

    modelo TEXT,

    status TEXT DEFAULT 'Planejado',

    criado_em TEXT,

    atualizado_em TEXT,

    FOREIGN KEY (responsavel)
        REFERENCES participantes(id)

)
""")

# ===========================================
# PROGRAMAÇÃO DO EVENTO
# ===========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS evento_itens (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    evento_id INTEGER NOT NULL,

    ordem INTEGER,

    horario TEXT,

    funcao TEXT,

    participante INTEGER,

    observacao TEXT,

    FOREIGN KEY (evento_id)
        REFERENCES eventos(id),

    FOREIGN KEY (participante)
        REFERENCES participantes(id)

)
""")

banco.commit()
banco.close()

print("Banco de eventos criado com sucesso!")