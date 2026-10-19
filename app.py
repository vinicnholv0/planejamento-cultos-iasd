from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
import sqlite3
from datetime import datetime
from functools import wraps
app = Flask(__name__)

app.secret_key = "planejamento_cultos_iasd_2026"

def conectar_banco():
    return sqlite3.connect("database/culto.db")

def login_obrigatorio(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if "usuario_id" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        banco = conectar_banco()
        cursor = banco.cursor()

        cursor.execute("""
            SELECT id, nome, usuario, senha, nivel
            FROM usuarios
            WHERE usuario=?
        """, (usuario,))

        dados = cursor.fetchone()

        banco.close()

        if dados and check_password_hash(dados[3], senha):

            session["usuario_id"] = dados[0]
            session["nome"] = dados[1]
            session["nivel"] = dados[4]

            return redirect("/")

        return render_template(
            "login.html",
            erro="Usuário ou senha inválidos."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
# ==========================
# DASHBOARD
# ==========================

@app.route("/")
@login_obrigatorio
def dashboard():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT id, data, tipo, tema
        FROM cultos
        ORDER BY data
    """)

    cultos = cursor.fetchall()

    banco.close()

    return render_template(
        "dashboard.html",
        cultos=cultos
    )


# ==========================
# LISTA DE CULTOS
# ==========================

@app.route("/cadastro-culto", methods=["GET", "POST"])
@login_obrigatorio
def cadastro_culto():
    
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT *
        FROM cultos
        ORDER BY data
    """)

    lista = cursor.fetchall()

    banco.close()

    return render_template(
        "cultos.html",
        cultos=lista
    )

# ==========================
# CADASTRAR CULTO
# ==========================

@app.route("/cultos")
@login_obrigatorio
def cultos():
    banco = conectar_banco()
    cursor = banco.cursor()

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO cultos
            (
                data,
                tipo,
                tema,
                hino_inicial,
                hino_final,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (

            request.form["data"],
            request.form["tipo"],
            request.form["tema"],
            request.form["hino_inicial"],
            request.form["hino_final"],
            request.form["observacoes"]

        ))

        banco.commit()
        banco.close()

        return redirect("/cultos")

    cursor.execute("""
        SELECT id, nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()

    return render_template(
        "cadastro_culto.html",
        participantes=participantes
    )

# ==========================
# DETALHES
# ==========================

@app.route("/culto/<int:id>")
@login_obrigatorio
def detalhes(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "SELECT * FROM cultos WHERE id=?",
        (id,)
    )

    culto = cursor.fetchone()

    banco.close()

    return render_template(
        "detalhes_culto.html",
        culto=culto
    )


# ==========================
# EDITAR
# ==========================

@app.route("/editar-culto/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_culto(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    if request.method == "POST":

        cursor.execute("""

            UPDATE cultos SET

            data=?,
            tipo=?,
            tema=?,
            hino_inicial=?,
            hino_final=?,
            observacoes=?

            WHERE id=?

        """,

        (

            request.form["data"],
            request.form["tipo"],
            request.form["tema"],
            request.form["hino_inicial"],
            request.form["hino_final"],
            request.form["observacoes"],
            id

        ))

        banco.commit()
        banco.close()
        return redirect("/cultos")

    cursor.execute(
        "SELECT * FROM cultos WHERE id=?",
        (id,)
    )

    culto = cursor.fetchone()

    banco.close()

    return render_template(
        "editar_culto.html",
        culto=culto
    )


# ==========================
# EXCLUIR
# ==========================

@app.route("/excluir-culto/<int:id>")
@login_obrigatorio
def excluir(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM cultos WHERE id=?",
        (id,)
    )

    banco.commit()
    banco.close()

    return redirect("/cultos")


# ==========================
# PARTICIPANTES
# ==========================

@app.route("/participantes")
@login_obrigatorio
def participantes():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""

        SELECT *
        FROM participantes
        ORDER BY nome

    """)

    participantes = cursor.fetchall()

    banco.close()

    return render_template(
        "participantes.html",
        participantes=participantes
    )


# ==========================
# NOVO PARTICIPANTE
# ==========================

@app.route("/cadastro-participante", methods=["GET", "POST"])
@login_obrigatorio
def cadastro_participante():

    banco = conectar_banco()
    cursor = banco.cursor()

    if request.method == "POST":

        cursor.execute("""

            INSERT INTO participantes
            (
                nome,
                telefone,
                email,
                observacoes,
                status
            )

            VALUES (?, ?, ?, ?, ?)

        """,

        (

            request.form["nome"],
            request.form["telefone"],
            request.form["email"],
            request.form["observacoes"],
            "Ativo"

        ))

        participante_id = cursor.lastrowid

        funcoes = request.form.getlist("funcoes")

        for funcao in funcoes:

            cursor.execute("""

                INSERT INTO participante_funcoes
                (
                    participante_id,
                    funcao_id
                )

                VALUES (?,?)

            """,

            (

                participante_id,
                funcao

            ))

        banco.commit()
        banco.close()
        return redirect("/participantes")

    cursor.execute("""
        SELECT *
        FROM funcoes
        ORDER BY nome
    """)

    funcoes = cursor.fetchall()

    banco.close()

    return render_template(
        "cadastro_participante.html",
        funcoes=funcoes
    )


# ==========================
# EDITAR PARTICIPANTE
# ==========================

@app.route("/editar-participante/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_participante(id):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "SELECT * FROM participantes WHERE id = ?",
        (id,)
    )
    participante = cursor.fetchone()

    if participante is None:
        banco.close()
        return "Participante não encontrado.", 404

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form.get("telefone", "")
        email = request.form.get("email", "")
        observacoes = request.form.get("observacoes", "")
        funcoes = request.form.getlist("funcoes")

        cursor.execute("""
            UPDATE participantes
            SET nome = ?, telefone = ?, email = ?, observacoes = ?
            WHERE id = ?
        """, (nome, telefone, email, observacoes, id))

        cursor.execute("""
            DELETE FROM participante_funcoes
            WHERE participante_id = ?
        """, (id,))

        for funcao_id in funcoes:
            cursor.execute("""
                INSERT INTO participante_funcoes
                (participante_id, funcao_id)
                VALUES (?, ?)
            """, (id, funcao_id))

        banco.commit()
        banco.close()
        return redirect("/participantes")

    cursor.execute("SELECT * FROM funcoes ORDER BY nome")
    funcoes = cursor.fetchall()

    cursor.execute("""
        SELECT funcao_id
        FROM participante_funcoes
        WHERE participante_id = ?
    """, (id,))
    funcoes_selecionadas = [str(linha[0]) for linha in cursor.fetchall()]

    banco.close()

    return render_template(
        "editar_participante.html",
        participante=participante,
        funcoes=funcoes,
        funcoes_selecionadas=funcoes_selecionadas
    )


# =========================
# EVENTOS
# =========================

@app.route("/eventos")
@login_obrigatorio
def eventos():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            data_inicio,
            hora_inicio,
            data_fim,
            hora_fim,
            local,
            responsavel,
            descricao,
            modelo
        FROM eventos
        ORDER BY data_inicio, hora_inicio
    """)

    lista_eventos = cursor.fetchall()

    banco.close()

    return render_template(
        "eventos.html",
        eventos=lista_eventos
    )
# ==========================
# ESCALAS MENSAIS
# ==========================

@app.route("/escalas")
@login_obrigatorio
def escalas():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            id,
            mes,
            ano,
            observacoes
        FROM escalas_mensais
        ORDER BY ano DESC, mes DESC
    """)

    escalas_mensais = cursor.fetchall()

    banco.close()

    return render_template(
        "escalas.html",
        escalas_mensais=escalas_mensais
    )

# ==========================
# ESCALA DE EVENTOS
# ==========================

@app.route("/escala-eventos")
@login_obrigatorio
def escala_eventos():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            data_inicio,
            hora_inicio,
            local,
            status
        FROM eventos
        ORDER BY data_inicio DESC, hora_inicio DESC
    """)

    eventos = cursor.fetchall()

    banco.close()

    return render_template(
        "escala_eventos.html",
        eventos=eventos
    )


# ==========================
# LISTA DE ESCALAS MENSAIS
# ==========================

@app.route("/escala-mensal-lista")
@login_obrigatorio
def lista_escalas_mensais():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            id,
            mes,
            ano,
            observacoes
        FROM escalas_mensais
        ORDER BY ano DESC, mes DESC
    """)

    escalas_mensais = cursor.fetchall()

    banco.close()

    return render_template(
        "escala_mensal_lista.html",
        escalas_mensais=escalas_mensais
    )

# ==========================
# ADICIONAR DIA À ESCALA MENSAL
# ==========================

@app.route("/adicionar-dia-escala/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def adicionar_dia_escala(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Busca a escala mensal
    cursor.execute("""
        SELECT
            id,
            mes,
            ano,
            observacoes
        FROM escalas_mensais
        WHERE id=?
    """, (id,))

    escala = cursor.fetchone()

    if escala is None:

        banco.close()

        return "Escala mensal não encontrada", 404


    # Salva o dia
    if request.method == "POST":

        data = request.form.get("data")
        tipo_culto = request.form.get("tipo_culto")

        canto = request.form.get("canto") or None
        pregador = request.form.get("pregador") or None
        colher_oferta = request.form.get("colher_oferta") or None
        professor_es = request.form.get("professor_es") or None
        diretor_es = request.form.get("diretor_es") or None
        observacoes = request.form.get("observacoes")


        cursor.execute("""
            INSERT INTO escala_mensal_dias
            (
                escala_id,
                data,
                tipo_culto,
                canto,
                pregador,
                colher_oferta,
                professor_es,
                diretor_es,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id,
            data,
            tipo_culto,
            canto,
            pregador,
            colher_oferta,
            professor_es,
            diretor_es,
            observacoes
        ))


        banco.commit()
        banco.close()

        return redirect(
            f"/escala-mensal/{id}"
        )


    # Busca participantes ativos
    cursor.execute("""
        SELECT
            id,
            nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()


    return render_template(
        "adicionar_dia_escala.html",
        escala=escala,
        participantes=participantes
    )

# ==========================
# EXCLUIR DIA DA ESCALA MENSAL
# ==========================

@app.route("/excluir-dia-escala/<int:id>")
@login_obrigatorio
def excluir_dia_escala(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Descobre a qual escala mensal esse dia pertence
    cursor.execute("""
        SELECT escala_id
        FROM escala_mensal_dias
        WHERE id=?
    """, (id,))

    resultado = cursor.fetchone()

    if resultado is None:

        banco.close()

        return "Dia da escala não encontrado", 404

    escala_id = resultado[0]


    # Exclui o dia
    cursor.execute("""
        DELETE FROM escala_mensal_dias
        WHERE id=?
    """, (id,))


    banco.commit()
    banco.close()


    return redirect(
        f"/escala-mensal/{escala_id}"
    )

# ==========================
# EDITAR DIA DA ESCALA MENSAL
# ==========================

@app.route("/editar-dia-escala/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_dia_escala(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Busca o dia da escala
    cursor.execute("""
        SELECT
            id,
            escala_id,
            data,
            tipo_culto,
            canto,
            pregador,
            colher_oferta,
            professor_es,
            diretor_es,
            observacoes
        FROM escala_mensal_dias
        WHERE id=?
    """, (id,))

    dia = cursor.fetchone()

    if dia is None:

        banco.close()

        return "Dia da escala não encontrado", 404


    escala_id = dia[1]


    # Salvar alterações
    if request.method == "POST":

        data = request.form.get("data")
        tipo_culto = request.form.get("tipo_culto")

        canto = request.form.get("canto") or None
        pregador = request.form.get("pregador") or None
        colher_oferta = request.form.get("colher_oferta") or None
        professor_es = request.form.get("professor_es") or None
        diretor_es = request.form.get("diretor_es") or None
        observacoes = request.form.get("observacoes")


        cursor.execute("""
            UPDATE escala_mensal_dias
            SET
                data=?,
                tipo_culto=?,
                canto=?,
                pregador=?,
                colher_oferta=?,
                professor_es=?,
                diretor_es=?,
                observacoes=?
            WHERE id=?
        """, (
            data,
            tipo_culto,
            canto,
            pregador,
            colher_oferta,
            professor_es,
            diretor_es,
            observacoes,
            id
        ))


        banco.commit()
        banco.close()


        return redirect(
            f"/escala-mensal/{escala_id}"
        )


    # Busca participantes
    cursor.execute("""
        SELECT
            id,
            nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()


    # Busca informações da escala
    cursor.execute("""
        SELECT
            id,
            mes,
            ano,
            observacoes
        FROM escalas_mensais
        WHERE id=?
    """, (escala_id,))

    escala = cursor.fetchone()

    banco.close()


    return render_template(
        "editar_dia_escala.html",
        dia=dia,
        escala=escala,
        participantes=participantes
    )

# ==========================
# NOVA ESCALA
# ==========================

@app.route("/nova-escala", methods=["GET", "POST"])
@login_obrigatorio
def nova_escala():

    banco = conectar_banco()
    cursor = banco.cursor()

    # ==========================
    # SALVAR ESCALA
    # ==========================

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO escalas (
                data,
                horario,
                evento,
                pregador,
                cantor,
                diretor,
                anciao,
                diacono,
                diaconisa,
                recepcao,
                sonoplastia,
                midia,
                infantil,
                observacoes
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            request.form.get("data"),

            request.form.get("horario"),

            request.form.get("evento"),

            request.form.get("pregador") or None,

            request.form.get("cantor") or None,

            request.form.get("diretor") or None,

            request.form.get("anciao") or None,

            request.form.get("diacono") or None,

            request.form.get("diaconisa") or None,

            request.form.get("recepcao") or None,

            request.form.get("sonoplastia") or None,

            request.form.get("midia") or None,

            request.form.get("infantil") or None,

            request.form.get("observacoes")

        ))

        banco.commit()

        banco.close()

        return redirect("/escalas")


    # ==========================
    # BUSCAR PARTICIPANTES
    # ==========================

    cursor.execute("""
        SELECT
            id,
            nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()

    return render_template(
        "nova_escala.html",
        participantes=participantes
    )

# ==========================
# ESCALA DE CANTORES
# ==========================

@app.route("/escala-cantores")
@login_obrigatorio
def escala_cantores():

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            escalas.id,
            escalas.data,
            escalas.horario,
            escalas.evento,
            participantes.nome
        FROM escalas
        LEFT JOIN participantes
            ON escalas.cantor = participantes.id
        ORDER BY escalas.data ASC, escalas.horario ASC
    """)

    escalas_cantores = cursor.fetchall()

    banco.close()

    return render_template(
        "escala_cantores.html",
        escalas_cantores=escalas_cantores
    )

# =========================
# HINOS
# =========================

@app.route("/hinos")
@login_obrigatorio
def hinos():
    return render_template("hinos.html")


# =========================
# SERMÕES
# =========================

@app.route("/sermoes")
@login_obrigatorio
def sermoes():
    return render_template("sermoes.html")


# =========================
# RELATÓRIOS
# =========================

@app.route("/relatorios")
@login_obrigatorio
def relatorios():
    return render_template("relatorios.html")


# =========================
# CONFIGURAÇÕES
# =========================

@app.route("/configuracoes")
@login_obrigatorio
def configuracoes():
    return render_template("configuracoes.html")

# =========================
# CADASTRO DE EVENTO
# =========================

@app.route("/cadastro-evento", methods=["GET", "POST"])
@login_obrigatorio
def cadastro_evento():

    banco = conectar_banco()
    cursor = banco.cursor()

    if request.method == "POST":

        tipo = request.form["tipo"]

        # Se o usuário escolheu "Outro"
        if tipo == "Outro":
            tipo = request.form["tipo_personalizado"]

        cursor.execute("""
            INSERT INTO eventos
            (
                nome,
                tipo,
                data_inicio,
                hora_inicio,
                data_fim,
                hora_fim,
                local,
                responsavel,
                descricao,
                modelo
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            request.form["nome"],
            tipo,
            request.form["data_inicio"],
            request.form["hora_inicio"],
            request.form["data_fim"],
            request.form["hora_fim"],
            request.form["local"],
            request.form["responsavel"],
            request.form["descricao"],
            ""

        ))

        banco.commit()

        evento_id = cursor.lastrowid

        banco.close()

        # Depois do cadastro vamos para os detalhes
        return redirect(f"/evento/{evento_id}")

    banco.close()

    return render_template(
        "cadastro_evento.html"
    )

# =========================
# DETALHES DO EVENTO
# =========================

@app.route("/evento/<int:id>")
@login_obrigatorio
def detalhes_evento(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            data_inicio,
            hora_inicio,
            data_fim,
            hora_fim,
            local,
            responsavel,
            descricao,
            modelo,
            status
        FROM eventos
        WHERE id=?
    """, (id,))

    evento = cursor.fetchone()

    banco.close()

    if evento is None:
        return "Evento não encontrado", 404

    return render_template(
        "detalhes_evento.html",
        evento=evento
    )

# =========================
# ALTERAR STATUS DO EVENTO
# =========================

@app.route("/alterar-status-evento/<int:id>", methods=["POST"])
@login_obrigatorio
def alterar_status_evento(id):

    status = request.form.get("status")

    status_permitidos = [
        "Planejado",
        "Realizado",
        "Cancelado"
    ]

    if status not in status_permitidos:
        return "Status inválido", 400

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE eventos
        SET status=?
        WHERE id=?
    """, (status, id))

    banco.commit()
    banco.close()

    return redirect(f"/evento/{id}")

# =========================
# PROGRAMAÇÃO DO EVENTO
# =========================

@app.route("/programacao-evento/<int:id>")
@login_obrigatorio
def programacao_evento(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # ==========================
    # BUSCAR EVENTO
    # ==========================

    cursor.execute("""
        SELECT *
        FROM eventos
        WHERE id=?
    """, (id,))

    evento = cursor.fetchone()

    if evento is None:
        banco.close()
        return "Evento não encontrado", 404

    # ==========================
    # BUSCAR PROGRAMAÇÃO
    # ==========================

    cursor.execute("""
        SELECT
            evento_itens.id,
            evento_itens.ordem,
            evento_itens.horario,
            evento_itens.funcao,
            participantes.nome,
            evento_itens.observacao
        FROM evento_itens

        LEFT JOIN participantes
        ON evento_itens.participante = participantes.id

        WHERE evento_itens.evento_id=?

        ORDER BY evento_itens.ordem, evento_itens.horario
    """, (id,))

    itens = cursor.fetchall()

    # ==========================
    # BUSCAR FUNÇÕES
    # ==========================

    cursor.execute("""
        SELECT id, nome
        FROM funcoes
        ORDER BY nome
    """)

    funcoes = cursor.fetchall()

    # ==========================
    # BUSCAR PARTICIPANTES ATIVOS
    # ==========================

    cursor.execute("""
        SELECT id, nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()

    return render_template(
        "programacao_evento.html",
        evento=evento,
        itens=itens,
        funcoes=funcoes,
        participantes=participantes
    )

    # Buscar itens já salvos
    cursor.execute("""
        SELECT
            ei.id,
            ei.ordem,
            ei.horario,
            ei.funcao,
            p.nome,
            ei.observacao
        FROM evento_itens ei

        LEFT JOIN participantes p
            ON CAST(ei.participante AS INTEGER) = p.id

        WHERE ei.evento_id=?

        ORDER BY ei.ordem, ei.horario
    """, (id,))

    itens = cursor.fetchall()

    # Buscar funções
    cursor.execute("""
        SELECT id, nome
        FROM funcoes
        ORDER BY nome
    """)

    funcoes = cursor.fetchall()

    # Buscar participantes ativos
    cursor.execute("""
        SELECT id, nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()

    return render_template(
        "programacao_evento.html",
        evento=evento,
        itens=itens,
        funcoes=funcoes,
        participantes=participantes
    )


# =========================
# ADICIONAR ITEM AO EVENTO
# =========================

@app.route(
    "/adicionar-item-evento/<int:id>",
    methods=["POST"]
)
@login_obrigatorio
def adicionar_item_evento(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Verificar se o evento existe
    cursor.execute("""
        SELECT id
        FROM eventos
        WHERE id=?
    """, (id,))

    evento = cursor.fetchone()

    if evento is None:
        banco.close()
        return "Evento não encontrado", 404

    # Descobrir próxima ordem
    cursor.execute("""
        SELECT COALESCE(MAX(ordem), 0) + 1
        FROM evento_itens
        WHERE evento_id=?
    """, (id,))

    ordem = cursor.fetchone()[0]

    horario = request.form.get("horario", "")
    funcao = request.form.get("funcao", "")
    participante = request.form.get("participante", "")
    observacao = request.form.get("observacao", "")

    if participante == "":
        participante = None

    # Salvar item
    cursor.execute("""
        INSERT INTO evento_itens
        (
            evento_id,
            horario,
            funcao,
            participante,
            observacao,
            ordem
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        id,
        horario,
        funcao,
        participante,
        observacao,
        ordem
    ))

    banco.commit()
    banco.close()

    return redirect(
        f"/programacao-evento/{id}"
    )
# =========================
# EXCLUIR ITEM
# =========================

@app.route("/excluir-item-evento/<int:item_id>")
@login_obrigatorio
def excluir_item_evento(item_id):

    banco = conectar_banco()
    cursor = banco.cursor()


    cursor.execute("""
        SELECT evento_id
        FROM evento_itens
        WHERE id=?
    """, (item_id,))

    resultado = cursor.fetchone()


    if resultado is None:

        banco.close()

        return "Item não encontrado", 404


    evento_id = resultado[0]


    cursor.execute("""
        DELETE FROM evento_itens
        WHERE id=?
    """, (item_id,))


    banco.commit()
    banco.close()


    return redirect(
        f"/programacao-evento/{evento_id}"
    )

# =========================
# PARTICIPANTES POR FUNÇÃO
# =========================

@app.route("/participantes-por-funcao/<int:funcao_id>")
@login_obrigatorio
def participantes_por_funcao(funcao_id):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nome
        FROM participantes p

        INNER JOIN participante_funcoes pf
            ON p.id = pf.participante_id

        WHERE pf.funcao_id = ?
        AND p.status = 'Ativo'

        ORDER BY p.nome
    """, (funcao_id,))

    participantes = cursor.fetchall()

    banco.close()

    return {
        "participantes": [
            {
                "id": participante[0],
                "nome": participante[1]
            }
            for participante in participantes
        ]
    }

# ==========================
# EDITAR ITEM DA PROGRAMAÇÃO
# ==========================

@app.route("/editar-item-evento/<int:item_id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_item_evento(item_id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # ==========================
    # BUSCAR ITEM
    # ==========================

    cursor.execute("""
        SELECT
            id,
            evento_id,
            horario,
            funcao,
            participante,
            observacao,
            ordem
        FROM evento_itens
        WHERE id=?
    """, (item_id,))

    item = cursor.fetchone()

    if item is None:
        banco.close()
        return "Item não encontrado", 404

    evento_id = item[1]

    # ==========================
    # SALVAR ALTERAÇÃO
    # ==========================

    if request.method == "POST":

        participante = request.form.get("participante")

        if participante == "":
            participante = None

        cursor.execute("""
            UPDATE evento_itens

            SET
                horario=?,
                funcao=?,
                participante=?,
                observacao=?

            WHERE id=?
        """, (

            request.form.get("horario"),
            request.form.get("funcao"),
            participante,
            request.form.get("observacao"),
            item_id

        ))

        banco.commit()
        banco.close()

        return redirect(
            f"/programacao-evento/{evento_id}"
        )

    # ==========================
    # BUSCAR FUNÇÕES
    # ==========================

    cursor.execute("""
        SELECT id, nome
        FROM funcoes
        ORDER BY nome
    """)

    funcoes = cursor.fetchall()

    # ==========================
    # BUSCAR PARTICIPANTES
    # ==========================

    cursor.execute("""
        SELECT id, nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()

    return render_template(
        "editar_item_evento.html",
        item=item,
        funcoes=funcoes,
        participantes=participantes,
        evento_id=evento_id
    )

# ==========================
# SUBIR ITEM DA PROGRAMAÇÃO
# ==========================

@app.route("/subir-item-evento/<int:item_id>")
@login_obrigatorio
def subir_item_evento(item_id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Busca o item atual
    cursor.execute("""
        SELECT id, evento_id, ordem
        FROM evento_itens
        WHERE id=?
    """, (item_id,))

    item = cursor.fetchone()

    if item is None:
        banco.close()
        return "Item não encontrado", 404

    evento_id = item[1]
    ordem_atual = item[2]

    # Procura o item imediatamente anterior
    cursor.execute("""
        SELECT id, ordem
        FROM evento_itens
        WHERE evento_id=?
        AND ordem < ?
        ORDER BY ordem DESC
        LIMIT 1
    """, (evento_id, ordem_atual))

    anterior = cursor.fetchone()

    if anterior:

        id_anterior = anterior[0]
        ordem_anterior = anterior[1]

        # Troca as ordens
        cursor.execute("""
            UPDATE evento_itens
            SET ordem=?
            WHERE id=?
        """, (ordem_anterior, item_id))

        cursor.execute("""
            UPDATE evento_itens
            SET ordem=?
            WHERE id=?
        """, (ordem_atual, id_anterior))

        banco.commit()

    banco.close()

    return redirect(
        f"/programacao-evento/{evento_id}"
    )


# ==========================
# DESCER ITEM DA PROGRAMAÇÃO
# ==========================

@app.route("/descer-item-evento/<int:item_id>")
@login_obrigatorio
def descer_item_evento(item_id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Busca o item atual
    cursor.execute("""
        SELECT id, evento_id, ordem
        FROM evento_itens
        WHERE id=?
    """, (item_id,))

    item = cursor.fetchone()

    if item is None:
        banco.close()
        return "Item não encontrado", 404

    evento_id = item[1]
    ordem_atual = item[2]

    # Procura o próximo item
    cursor.execute("""
        SELECT id, ordem
        FROM evento_itens
        WHERE evento_id=?
        AND ordem > ?
        ORDER BY ordem ASC
        LIMIT 1
    """, (evento_id, ordem_atual))

    proximo = cursor.fetchone()

    if proximo:

        id_proximo = proximo[0]
        ordem_proximo = proximo[1]

        # Troca as ordens
        cursor.execute("""
            UPDATE evento_itens
            SET ordem=?
            WHERE id=?
        """, (ordem_proximo, item_id))

        cursor.execute("""
            UPDATE evento_itens
            SET ordem=?
            WHERE id=?
        """, (ordem_atual, id_proximo))

        banco.commit()

    banco.close()

    return redirect(
        f"/programacao-evento/{evento_id}"
    )

# ==========================
# VISUALIZAR PROGRAMAÇÃO
# ==========================

@app.route("/visualizar-programacao-evento/<int:id>")
@login_obrigatorio
def visualizar_programacao_evento(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Busca o evento
    cursor.execute("""
        SELECT *
        FROM eventos
        WHERE id=?
    """, (id,))

    evento = cursor.fetchone()

    if evento is None:
        banco.close()
        return "Evento não encontrado", 404

    # Busca a programação
    cursor.execute("""
        SELECT
            horario,
            funcao,
            participante,
            observacao,
            ordem
        FROM evento_itens
        WHERE evento_id=?
        ORDER BY ordem ASC
    """, (id,))

    itens = cursor.fetchall()

    # Buscar nomes dos participantes
    programacao = []

    for item in itens:

        horario = item[0]
        funcao = item[1]
        participante_id = item[2]
        observacao = item[3]
        ordem = item[4]

        participante_nome = ""

        if participante_id:

            cursor.execute("""
                SELECT nome
                FROM participantes
                WHERE id=?
            """, (participante_id,))

            resultado = cursor.fetchone()

            if resultado:
                participante_nome = resultado[0]

        programacao.append({
            "horario": horario,
            "funcao": funcao,
            "participante": participante_nome,
            "observacao": observacao,
            "ordem": ordem
        })

    banco.close()

    return render_template(
        "visualizar_programacao_evento.html",
        evento=evento,
        programacao=programacao
    )

# ==========================
# EXCLUIR EVENTO
# ==========================

@app.route("/excluir-evento/<int:id>")
@login_obrigatorio
def excluir_evento(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Verifica se o evento existe
    cursor.execute("""
        SELECT id
        FROM eventos
        WHERE id=?
    """, (id,))

    evento = cursor.fetchone()

    if evento is None:
        banco.close()
        return "Evento não encontrado", 404

    # Exclui os itens da programação
    cursor.execute("""
        DELETE FROM evento_itens
        WHERE evento_id=?
    """, (id,))

    # Exclui o evento
    cursor.execute("""
        DELETE FROM eventos
        WHERE id=?
    """, (id,))

    banco.commit()
    banco.close()

    return redirect("/eventos")

# ==========================================
# NOVA ESCALA MENSAL
# ==========================================

@app.route("/nova-escala-mensal", methods=["GET", "POST"])
@login_obrigatorio
def nova_escala_mensal():

    banco = conectar_banco()
    cursor = banco.cursor()

    if request.method == "POST":

        mes = request.form.get("mes")
        ano = request.form.get("ano")
        observacoes = request.form.get("observacoes")

        try:

            cursor.execute("""
                INSERT INTO escalas_mensais
                (
                    mes,
                    ano,
                    observacoes
                )
                VALUES (?, ?, ?)
            """, (
                mes,
                ano,
                observacoes
            ))

            escala_id = cursor.lastrowid

            banco.commit()
            banco.close()

            return redirect(
                f"/escala-mensal/{escala_id}"
            )

        except sqlite3.IntegrityError:

            banco.close()

            return "Essa escala mensal já existe.", 400

    banco.close()

    return render_template(
        "nova_escala_mensal.html"
    )

# ==========================
# VISUALIZAR ESCALA MENSAL
# ==========================

@app.route("/escala-mensal/<int:id>")
@login_obrigatorio
def escala_mensal(id):

    banco = conectar_banco()
    cursor = banco.cursor()

    # Busca a escala mensal
    cursor.execute("""
        SELECT
            id,
            mes,
            ano,
            observacoes
        FROM escalas_mensais
        WHERE id=?
    """, (id,))

    escala = cursor.fetchone()

    if escala is None:

        banco.close()

        return "Escala mensal não encontrada", 404


    # Busca os dias da escala
    cursor.execute("""
        SELECT
            id,
            data,
            tipo_culto,
            canto,
            pregador,
            colher_oferta,
            professor_es,
            diretor_es,
            observacoes
        FROM escala_mensal_dias
        WHERE escala_id=?
        ORDER BY data
    """, (id,))

    dias = cursor.fetchall()


    # Busca participantes
    cursor.execute("""
        SELECT
            id,
            nome
        FROM participantes
        WHERE status='Ativo'
        ORDER BY nome
    """)

    participantes = cursor.fetchall()

    banco.close()


    # Cria um dicionário:
    # ID do participante -> Nome

    nomes = {}

    for participante in participantes:

        nomes[participante[0]] = participante[1]


    # Cria um dicionário:
    # ID do dia -> Dia da semana

    from datetime import datetime

    dias_semana = {}

    nomes_dias = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo"
    ]

    for dia in dias:

        data = datetime.strptime(
            dia[1],
            "%Y-%m-%d"
        )

        dias_semana[dia[0]] = nomes_dias[data.weekday()]


    return render_template(
        "escala_mensal.html",
        escala=escala,
        dias=dias,
        nomes=nomes,
        dias_semana=dias_semana
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)