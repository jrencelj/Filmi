import pandas as pd
import sqlite3 as dbapi
import json

db = dbapi.connect("filmi.db")

with open("filmi.json", 'r') as f:
    filmi = json.load(f)

certifikati = set()
for kljuc, vrednost in filmi.items():
    certifikati.add(vrednost["Rated"])

def cetifikati_napolni():
    with db as cursor:
        for cer in list(certifikati):
            cursor.execute("""
                INSERT INTO certifikat (sifra) VALUES(:cer)
            """,{"cer" : cer})

def filmi_napolni():
    with db as cursor:
        for film, podatki in filmi.items():
            naslov = film
            dolzina = podatki["Runtime"].replace(" min", "")
            leto = podatki["Year"]
            cer = podatki["Rated"]
            cursor.execute("""
                INSERT INTO film (naslov, dolzina, leto, certifikat_id) 
                VALUES(:naslov, :dolzina, :leto, (SELECT id FROM certifikat WHERE sifra = :cer))
            """, {"naslov" : naslov, "dolzina" : dolzina, "leto" : leto, "cer" : cer})
    



