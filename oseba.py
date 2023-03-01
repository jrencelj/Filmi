import sqlite3 as dbapi

class Oseba:
    def __init__(self, id, ime_priimek, imdb_id_oseba, url_slika=None):
        self._id = id
        self._ime_priimek = ime_priimek
        self._imdb_id_oseba = imdb_id_oseba
        self._url_slika = url_slika

    def shrani_oseba(self):
        '''Shrani osebo v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT OR IGNORE INTO oseba (ime_priimek, url_slika, imdb_id_oseba)
            VALUES (?, ?, ?)
            """, [self._ime_priimek, self._url_slika, self._imdb_id_oseba])

    @staticmethod
    def pridobi_oseba_id(imdb_id_oseba):
        '''Pridobi id osebe iz baze'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM oseba
                WHERE imdb_id_oseba=?
            """, [imdb_id_oseba])
            id = cursor.fetchone()[0]
            return id

    
    
    @staticmethod
    def pridobi_oseba_po_id(id):
        """Pridobi osebo po id."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT * FROM oseba WHERE id = ?;
            """, [id])
            podatki = cursor.fetchone()
        return Oseba(podatki[0], podatki[1], podatki[3], podatki[2])

    @property
    def id(self):
        return self._id
    @property
    def ime_priimek(self):
        return self._ime_priimek

    @property
    def imdb_id_oseba(self):
        return self._imdb_id_oseba

    @property
    def url_slika(self):
        return self._url_slika

    @ime_priimek.setter
    def ime_priimek(self, vrednost):
        self._ime_priimek = vrednost

    @imdb_id_oseba.setter
    def imdb_id_oseba(self, vrednost):
        self._imdb_id_oseba = vrednost

    @url_slika.setter
    def url_slika(self, vrednost):
        self._url_slika = vrednost
