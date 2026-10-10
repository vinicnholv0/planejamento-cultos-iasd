import sqlite3

banco = sqlite3.connect("database/culto.db")
cursor = banco.cursor()

# ==========================================
# ESCALAS MENSAIS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS escalas_mensais (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    mes INTEGER NOT NULL,

    ano INTEGER NOT NULL,

    observacoes TEXT,

    UNIQUE(mes, ano)

)
""")


# ==========================================
# DIAS DA ESCALA MENSAL
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS escala_mensal_dias (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    escala_id INTEGER NOT NULL,

    data TEXT NOT NULL,

    tipo_culto TEXT,

    canto INTEGER,

    pregador INTEGER,

    colher_oferta INTEGER,

    professor_es INTEGER,

    diretor_es INTEGER,

    observacoes TEXT,

    FOREIGN KEY (escala_id)
        REFERENCES escalas_mensais(id),

    FOREIGN KEY (canto)
        REFERENCES participantes(id),

    FOREIGN KEY (pregador)
        REFERENCES participantes(id),

    FOREIGN KEY (colher_oferta)
        REFERENCES participantes(id),

    FOREIGN KEY (professor_es)
        REFERENCES participantes(id),

    FOREIGN KEY (diretor_es)
        REFERENCES participantes(id)

)
""")


banco.commit()
banco.close()

print("Estrutura da escala mensal criada com sucesso!")