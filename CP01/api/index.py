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
<!doctype html>
<html>
  <head>
    <title>SQLgard - RPG Engine</title>

    <style>
      body {
        font-family: Arial, Helvetica, sans-serif;
        background-color: #f5f5f5;
        text-align: center;
        justify-content: center;
      }

      h1 {
        margin-bottom: 5px;
      }

      .next {
        background-color: #423ce7;
        color: white;
        border: none;
        padding: 12px 25px;
        font-size: 16px;
        cursor: pointer;
      }

      .next:hover {
        background-color: #2c28aa;
      }

      .reset {
        background-color: red;
        color: white;
        border: none;
        padding: 12px 25px;
        font-size: 16px;
        cursor: pointer;
      }

      .reset:hover {
        background-color: #aa0000;
      }

      table {
        border-collapse: collapse;
        width: 70%;
        margin-top: 20px;
        background-color: #d9d9d9;
      }

      th,
      td {
        border: 1px solid #c0c0c0;
        padding: 10px;
        text-align: left;
        background-color: #eee;
      }

      th {
        background-color: #d0d0d0;
      }

      .caido {
        background-color: #e5bcbc;
        font-weight: bold;
      }
    </style>
  </head>

  <body>
    <div>
      <h1>SQLgard - RPG Engine</h1>

      <p>O Despertar do Kernel Ancestral</p>

      <p><i>Uma nevoa venenosa drena a vida de todos os herois...</i></p>
    </div>
    <div
      style="
        flex-direction: columns;
        display: flex;
        gap: 10px;
        justify-content: center;
      "
    >
      <form action="/processar" method="post">
        <button type="submit" class="next">Proximo Turno</button>
      </form>
      <form action="/resetar" method="post">
        <button type="submit" class="reset">
          Resetar Jogo
        </button>
      </form>
    </div>
    <div style="margin-left: auto; margin-right: 0; width: 80%;">
      <table>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Classe</th>
          <th>HP</th>
          <th>Barra HP</th>
          <th>Status</th>
        </tr>

        {% for h in herois %}
        <tr>
          <td>{{h[0]}}</td>
          <td>{{h[1]}}</td>
          <td>{{h[2]}}</td>

          <td>{{h[3]}}/{{h[4]}}</td>

          <td>
            <progress value="{{h[3]}}" max="{{h[4]}}"></progress>
          </td>

          <td class="{% if h[5] == 'CAIDO' %}caido{% endif %}">{{h[5]}}</td>
        </tr>
        {% endfor %}
      </table>
    </div>
  </body>
</html>
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