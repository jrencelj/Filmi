import sqlite3 as dbapi

db = dbapi.connect("filmi.db")

# Ustvarimo tabele
def ustvari_tabele():

    with db as cursor:

        # uporabnik_tip (#1)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uporabnik_tip
            (
                id INTEGER PRIMARY KEY,
                sifra INTEGER,
                naziv VARCHAR(200)
            );
            """)    

        # uporabnik (#2)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uporabnik
            (
                id INTEGER PRIMARY KEY,
                e_naslov VARCHAR(250),
                uporabnisko_ime VARCHAR(100),
                datum_rojstva DATE,
                geslo VARCHAR(255),
                sol VARCHAR(5),
                uporabnik_tip_id INTEGER,
                FOREIGN KEY (uporabnik_tip_id) REFERENCES uporabnik_tip(id)
            );
        """)

        # film (#3)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS film
            (
                id INTEGER PRIMARY KEY,
                naslov VARCHAR(255),
                dolzina INTEGER,
                leto INTEGER,
                certifikat_id INTEGER,
                FOREIGN KEY (certifikat_id) REFERENCES certifikat(id)
            );
            """)

        # certifikat (#4)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS certifikat
            (
                id INTEGER PRIMARY KEY,
                sifra VARCHAR(30)
            );
            """)

        # oseba (#5)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS oseba
            (
                id INTEGER PRIMARY KEY,
                ime VARCHAR(60),
                priimek VARCHAR(150),
                datum_rojstva DATE
            );
        """)

        # vloga (#6)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vloga
            (
                id INTEGER PRIMARY KEY,
                sifra INTEGER,
                naziv VARCHAR(100)
            );
        """)

        # kinoteka (#7)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kinoteka
            (
                id INTEGER PRIMARY KEY,
                ime VARCHAR(100),
                url VARCHAR(200)
            );
        """)

        # film_kinoteka (#8)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS film_kinoteka
            (
                id INTEGER PRIMARY KEY,
                kinoteka_id INTEGER,
                film_id INTEGER,
                FOREIGN KEY (film_id) REFERENCES film(id),
                FOREIGN KEY (kinoteka_id) REFERENCES kinoteka(id)
            );
        """)

        # komentar_tip (#9)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS komentar_tip
            (
                id INTEGER PRIMARY KEY,
                sifra INTEGER,
                naziv VARCHAR(50)
            );
        """)

        # komentar (#10)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS komentar
            (
                id INTEGER PRIMARY KEY,
                ocena SMALLINT,
                ura_datum DATETIME,
                naslov VARCHAR(300),
                opis TEXT,
                komentar_tip_id INTEGER,
                uporabnik_id INTEGER,
                film_id INTEGER,
                FOREIGN KEY (komentar_tip_id) REFERENCES komentar_tip(id),
                FOREIGN KEY (uporabnik_id) REFERENCES uporabnik(id),
                FOREIGN KEY (film_id) REFERENCES film(id)
            );
        """)

        #film_oseba (#11)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS film_oseba
            (
                id INTEGER PRIMARY KEY,
                oseba_id INT,
                film_id INT,
                vloga_id INT,
                FOREIGN KEY (oseba_id) REFERENCES oseba(id),
                FOREIGN KEY (film_id) REFERENCES film(id),
                FOREIGN KEY (vloga_id) REFERENCES vloga(id)
            );
        """)

        #zvrst (#12)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zvrst
            (
                id INTEGER PRIMARY KEY,
                ime_zvrsti VARCHAR(250),
                opis TEXT
            );
        """)

        #film_zvrst (#13)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS film_zvrst
            (
                id INTEGER PRIMARY KEY,
                film_id INTEGER,
                zvrst_id INTEGER,
                FOREIGN KEY (film_id) REFERENCES film(id),
                FOREIGN KEY (zvrst_id) REFERENCES zvrst(id)
            );
        """)

ustvari_tabele()