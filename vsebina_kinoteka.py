import sqlite3 as dbapi
class Vsebina_Kinoteka:
    def __init__(self, id, kinoteka_id, vsebina_id):
        self._id = id
        self._kinoteka_id = kinoteka_id
        self._vsebina_id = vsebina_id

    # GET IN SET METODE
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, vrednost):
        self._id = vrednost

    @property
    def kinoteka_id(self):
        return self._kinoteka_id
    
    @kinoteka_id.setter
    def kinoteka_id(self, vrednost):
        self._kinoteka_id = vrednost

    @property
    def vsebina_id(self):
        return self._vsebina_id
    
    @vsebina_id.setter
    def vsebina_id(self, vrednost):
        self._vsebina_id = vrednost

    # SQL
    def shrani_kinoteka_vsebina(self):
        """Shrani vebina_kinoteka v bazo."""
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
                INSERT INTO vsebina_kinoteka (kinoteka_id, vsebina_id)
                VALUES (?, ?);
            """, [self.kinoteka_id, self.vsebina_id])
