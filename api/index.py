from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import oracledb
import os
from mangum import Mangum

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_connection():
    return oracledb.connect(
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hero_id, name, player_class, hp, hp_max, status
        FROM TB_HEROIS
        ORDER BY hero_id
    """)

    heroes = []

    for row in cursor:
        heroes.append(Hero(*row))

    cursor.close()
    conn.close()

    return heroes


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    heroes = get_all_heroes()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "heroes": heroes}
    )


@app.get("/turn")
def next_turn():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(plsql)
    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse("/", status_code=303)


@app.get("/reset")
def reset():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(plsql_reset)
    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse("/", status_code=303)


handler = Mangum(app)