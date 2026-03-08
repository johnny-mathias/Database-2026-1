import streamlit as st
import oracledb
import os

conn = oracledb.connect(
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    dsn=os.environ["DB_DSN"]
)

cursor = conn.cursor()

plsql = """
DECLARE
    v_dano_nevoa NUMBER := 10;
BEGIN
    FOR r IN (
        SELECT id_heroi, hp_atual
        FROM TB_HEROIS
        WHERE status = 'ATIVO'
    ) LOOP
    
        UPDATE TB_HEROIS
        SET hp_atual = hp_atual - v_dano_nevoa
        WHERE id_heroi = r.id_heroi;

        UPDATE TB_HEROIS
        SET status = 'CAIDO'
        WHERE id_heroi = r.id_heroi
        AND hp_atual - v_dano_nevoa <= 0;

    END LOOP;

END;
"""

cursor.execute(plsql)
conn.commit()

print("Conectado ao banco!")

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
    cursor.execute("SELECT hero_id, name, player_class, hp, max_hp, status FROM heroes")
    heroes = []
    for row in cursor:
        hero = Hero(row[0], row[1], row[2], row[3], row[4], row[5])
        heroes.append(hero)
    return heroes

