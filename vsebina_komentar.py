import sqlite3 as dbapi

class Vsebina_Komentar:

    def __init__(self, id, vsebina_id, komentar_id):
        self._id = id
        self._vsebina_id = vsebina_id
        self._komentar_id = komentar_id

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
    def komentar_id(self):
        return self._komentar_id
    
    @komentar_id.setter
    def komentar_id(self, vrednost):
        self._komentar_id = vrednost

    def shrani_vsebina_komentar(self):
        """Shrani vsebina-komentar v bazo."""
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
                INSERT INTO vsebina_komentar (vsebina_id, komentar_id)
                VALUES (?,?)
            """,[self.vsebina_id, self.komentar_id])