import sqlite3

banco = sqlite3.connect("database/culto.db")
cursor = banco.cursor()

# ==========================================
# ADICIONAR STATUS
# ==========================================

try:
    cursor.execute("""
        ALTER TABLE eventos
        ADD COLUMN status TEXT DEFAULT 'Planejado'
    """)

    print("Coluna status adicionada com sucesso!")

except sqlite3.OperationalError:
    print("A coluna status já existe.")


# ==========================================
# ADICIONAR DATA DE CRIAÇÃO
# ==========================================

try:
    cursor.execute("""
        ALTER TABLE eventos
        ADD COLUMN criado_em TEXT
    """)

    print("Coluna criado_em adicionada com sucesso!")

except sqlite3.OperationalError:
    print("A coluna criado_em já existe.")


# ==========================================
# ADICIONAR DATA DE ATUALIZAÇÃO
# ==========================================

try:
    cursor.execute("""
        ALTER TABLE eventos
        ADD COLUMN atualizado_em TEXT
    """)

    print("Coluna atualizado_em adicionada com sucesso!")

except sqlite3.OperationalError:
    print("A coluna atualizado_em já existe.")


banco.commit()
banco.close()

print()
print("Banco de eventos atualizado com sucesso!")