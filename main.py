import streamlit as st
import oracledb
import os

# conexão com banco
conn = oracledb.connect(
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    dsn=os.environ["DB_DSN"]
)

cursor = conn.cursor()

# bloco plsql
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

# classe hero
class Hero:
    def __init__(self, hero_id, name, player_class, hp, max_hp, status):
        self.hero_id = hero_id
        self.name = name
        self.player_class = player_class
        self.hp = hp
        self.max_hp = max_hp
        self.status = status


# buscar herois
def get_all_heroes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_heroi, nome, classe, hp_atual, hp_max, status
        FROM TB_HEROIS
        ORDER BY id_heroi
    """)

    heroes = []

    for row in cursor:
        hero = Hero(row[0], row[1], row[2], row[3], row[4], row[5])
        heroes.append(hero)

    return heroes


# executar turno
def process_turn():
    cursor.execute(plsql)
    conn.commit()


# -------- STREAMLIT UI --------

st.title("SQLgard - RPG Engine")
st.subheader("O Despertar do Kernel Ancestral")
st.write("*Uma névoa venenosa drena a vida de todos os heróis...*")
st.set_page_config(layout="wide")

# botão
if st.button("Próximo Turno"):
    process_turn()
    st.rerun()


# tabela de herois
heroes = get_all_heroes()

col1, col2, col3, col4, col5, col6 = st.columns([1,2,2,2,3,2])

col1.write("ID")
col2.write("Nome")
col3.write("Classe")
col4.write("HP")
col5.write("Barra HP")
col6.write("Status")

for hero in heroes:

    c1, c2, c3, c4, c5, c6 = st.columns([1,2,2,2,3,2])

    c1.write(hero.hero_id)
    c2.write(hero.name)
    c3.write(hero.player_class)
    c4.write(f"{hero.hp}/{hero.max_hp}")

    # barra hp
    hp_percent = hero.hp / hero.max_hp if hero.max_hp > 0 else 0
    c5.progress(hp_percent)

    # status
    if hero.status == "CAIDO":
        c6.error("CAIDO")
    else:
        c6.success("ATIVO")