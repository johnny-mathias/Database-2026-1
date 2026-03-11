from flask import Flask, request, redirect, render_template_string
import oracledb
import os

app = Flask(__name__)

def get_conn():
    return oracledb.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dsn=os.environ["DB_DSN"]
    )

HTML = """
<h1>SQLgard - RPG Engine</h1>
<h3>O Despertar do Kernel Ancestral</h3>

<p><i>Uma nevoa venenosa drena a vida de todos os herois...</i></p>

<form action="/processar" method="post">
<button type="submit">Proximo Turno</button>
</form>
<form action="/resetar" method="post">
<button type="submit" style="background-color:red;color:white">Resetar Jogo</button>
</form>

<br>

<table border="1" cellpadding="5">
<tr>
<th>ID</th>
<th>Nome</th>
<th>Classe</th>
<th>HP</th>
<th>Status</th>
</tr>

{% for h in herois %}
<tr>
<td>{{h[0]}}</td>
<td>{{h[1]}}</td>
<td>{{h[2]}}</td>
<td>{{h[3]}}/{{h[4]}}</td>
<td>{{h[5]}}</td>
</tr>
{% endfor %}

</table>
"""

@app.route("/")
def index():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT id_heroi, nome, classe, hp_atual, hp_max, status
    FROM TB_HEROIS
    ORDER BY id_heroi
    """)

    herois = cur.fetchall()

    conn.close()

    return render_template_string(HTML, herois=herois)


@app.route("/processar", methods=["POST"])
def processar():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""

DECLARE

    v_dano_nevoa NUMBER := 10;

    CURSOR c_herois IS
        SELECT id_heroi, hp_atual, hp_max
        FROM TB_HEROIS
        WHERE status = 'ATIVO'
        FOR UPDATE;

    v_hp NUMBER;

BEGIN

    FOR r IN c_herois LOOP

        v_hp := r.hp_atual - v_dano_nevoa;

        IF v_hp <= 0 THEN
            UPDATE TB_HEROIS
            SET hp_atual = 0,
                status = 'CAIDO'
            WHERE id_heroi = r.id_heroi;
        ELSE
            UPDATE TB_HEROIS
            SET hp_atual = v_hp
            WHERE id_heroi = r.id_heroi;
        END IF;

    END LOOP;

END;

""")

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/resetar", methods=["POST"])
def resetar():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""

    UPDATE TB_HEROIS
    SET hp_atual = hp_max,
        status = 'ATIVO'

    """)

    conn.commit()
    conn.close()

    return redirect("/")


app = app