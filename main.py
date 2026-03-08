import streamlit as st
import oracledb
import os

user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
dsn = os.environ.get("DB_DSN")

connection = oracledb.connect(
    user=user,
    password=password,
    dsn=dsn
)

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
    cursor = connection.cursor()
    cursor.execute("SELECT hero_id, name, player_class, hp, max_hp, status FROM heroes")
    heroes = []
    for row in cursor:
        hero = Hero(row[0], row[1], row[2], row[3], row[4], row[5])
        heroes.append(hero)
    return heroes

