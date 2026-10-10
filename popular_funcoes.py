import sqlite3
import sqlite3

banco = sqlite3.connect("database/culto.db")
cursor = banco.cursor()

funcoes = [
    "Pastor",
    "Ancião",
    "Diretor de Culto",
    "Diácono",
    "Diaconisa",
    "Cantor",
    "Organista",
    "Música Especial",
    "Sonoplastia",
    "Mídia",
    "Recepção",
    "Ministério Infantil"
]

for funcao in funcoes:
    cursor.execute("""
        INSERT OR IGNORE INTO funcoes (nome)
        VALUES (?)
    """, (funcao,))

# Remove funções que não queremos mais utilizar
cursor.execute("""
    DELETE FROM funcoes
    WHERE nome IN ('Pianista', 'Louvor')
""")

banco.commit()
banco.close()

print("Funções atualizadas com sucesso!")