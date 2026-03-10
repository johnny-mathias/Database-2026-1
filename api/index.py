from flask import Flask, render_template, redirect, request
import oracledb
import os

app = Flask(__name__)

conn = oracledb.connect(
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    dsn=os.environ["DB_DSN"]
)

plsql = """
DECLARE
    v_dano_nevoa NUMBER := 10;
BEGIN
    FOR r IN (
        SELECT hero_id, hp
        FROM TB_HEROIS
        WHERE status = 'ATIVO'
    ) LOOP

        UPDATE TB_HEROIS
        SET hp = GREATEST(hp - v_dano_nevoa, 0)
        WHERE hero_id = r.hero_id;

        UPDATE TB_HEROIS
        SET status = 'CAIDO'
        WHERE hero_id = r.hero_id
        AND hp = 0;

    END LOOP;
END;
"""

plsql_reset = """
BEGIN
    UPDATE TB_HEROIS
    SET hp = hp_max,
        status = 'ATIVO';
END;
"""


class Hero:
    def __init__(self, hero_id, name, player_class, hp, max_hp, status):
        self.hero_id = hero_id
        self.name = name
        self.player_class = player_class
        self.hp = hp
        self.max_hp = max_hp
        self.status = status


def get_all_heroes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hero_id, name, player_class, hp, hp_max, status
        FROM TB_HEROIS
        ORDER BY hero_id
    """)

    heroes = []

    for row in cursor:
        heroes.append(Hero(*row))

    return heroes


@app.route("/")
def index():
    heroes = get_all_heroes()
    return render_template("index.html", heroes=heroes)


@app.route("/turn")
def next_turn():
    cursor = conn.cursor()
    cursor.execute(plsql)
    conn.commit()
    return redirect("/")


@app.route("/reset")
def reset():
    cursor = conn.cursor()
    cursor.execute(plsql_reset)
    conn.commit()
    return redirect("/")