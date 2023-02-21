import sqlite3 as dbapi

class Vsebina_Imdb_Komentar:
    def __init__(self, id, vsebina_id, imdb_komentar_id):
        self._id = id
        self._vsebina_id = vsebina_id
        self._imdb_komentar_id = imdb_komentar_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, vrednost):
        self._id = vrednost
    
    @property
    def vsebina_id(self):
        return self._vsebina_id

    @vsebina_id.setter
    def vsebina_id(self, vrednost):
        self._vsebina_id = vrednost
    
    @property
    def imdb_komentar_id(self):
        return self._imdb_komentar_id

    @imdb_komentar_id.setter
    def imdb_komentar_id(self, vrednost):
        self._imdb_komentar_id = vrednost

    def shrani_vsebina_imdb_komentar(self):
        """Shrani, naredi povezavo v vmesni tabeli."""
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
            INSERT INTO vsebina_imdb_komentar(vsebina_id, imdb_komentar_id)
            VALUES (?, ?)
            """, [self.vsebina_id, self.imdb_komentar_id])

    