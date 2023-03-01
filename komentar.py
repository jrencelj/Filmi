from film import Film
from uporabnik import Uporabnik
import sqlite3 as dbapi

class Komentar:
    def __init__(self, id, ocena, ura_datum, naslov_komentar, besedilo_komentar, uporabnik_id):
        self._id = id
        self._ocena = ocena
        self._ura_datum = ura_datum
        self._naslov_komentar = naslov_komentar
        self._besedilo_komentar = besedilo_komentar
        self._uporabnik_id = uporabnik_id
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, vrednost):
        self._id = vrednost

    @property
    def ocena(self):
        return self._ocena
    
    @ocena.setter
    def ocena(self, vrednost):
        self._ocena = vrednost

    @property
    def ura_datum(self):
        return self._ura_datum
    
    @ura_datum.setter
    def ura_datum(self, vrednost):
        self._ura_datum = vrednost
    
    @property
    def naslov_komentar(self):
        return self._naslov_komentar
    
    @naslov_komentar.setter
    def naslov_komentar(self, vrednost):
        self._naslov_komentar = vrednost
    
    @property
    def besedilo_komentar(self):
        return self._besedilo_komentar
    
    @besedilo_komentar.setter
    def besedilo_komentar(self, vrednost):
        self._besedilo_komentar = vrednost
    
    @property
    def uporabnik_id(self):
        return self._uporabnik_id
    
    @uporabnik_id.setter
    def uporabnik_id(self, vrednost):
        self._uporabnik_id = vrednost
    

    # SQL
    def shrani_komentar(self):
        """Shrani komentar, ki ga vpiše uporabnik, v bazo."""
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
                INSERT INTO komentar (ocena, ura_datum, naslov_komentar, besedilo_komentar, uporabnik_id)
                VALUES (?,?,?,?,?)
            """, [self.ocena, self.ura_datum, self.naslov_komentar, self.besedilo_komentar, self.uporabnik_id])

    @staticmethod
    def pridobi_id_komentar(uporabnik_id, besedilo, ura_datum, ocena):
        """Pridobi id komentarja glede na dane parametre funkcije."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT id FROM komentar WHERE uporabnik_id=? AND besedilo_komentar=? AND ura_datum=? AND ocena=?
            """,[uporabnik_id, besedilo, ura_datum, ocena])
            id = cursor.fetchone()[0]
        return id
    
    @staticmethod
    def pridobi_komentarje_za_vsebino(vsebina_id):
        """Pridobi komentarje za dano vsebino."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT t2.*, t3.uporabnisko_ime FROM vsebina_komentar AS t1 INNER JOIN komentar AS t2 ON t1.komentar_id = t2.id INNER JOIN uporabnik AS t3 ON t2.uporabnik_id = t3.id
                WHERE t1.vsebina_id = ?;
            """, [vsebina_id])
            podatki = cursor.fetchall()
        return [
            [Komentar(podatek[0], podatek[1], podatek[2], podatek[3], podatek[4], podatek[5]), podatek[6]]
            for podatek in podatki
        ]