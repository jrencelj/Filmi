import sqlite3 as dbapi
class Vsebina_Oseba:
    def __init__(self, id, vloga, oseba_id, vsebina_id, vloga_tip_id):
        self._id = id
        self._vloga = vloga
        self._oseba_id = oseba_id
        self._vsebina_id = vsebina_id
        self._vloga_tip_id = vloga_tip_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, vrednost):
        self._id = vrednost

    @property
    def vloga(self):
        return self._vloga

    @vloga.setter
    def vloga(self, vrednost):
        self._vloga = vrednost

    @property
    def oseba_id(self):
        return self._oseba_id

    @oseba_id.setter
    def oseba_id(self, vrednost):
        self._oseba_id = vrednost

    @property
    def vsebina_id(self):
        return self._vsebina_id

    @vsebina_id.setter
    def vsebina_id(self, vrednost):
        self._vsebina_id = vrednost

    @property
    def vloga_tip_id(self):
        return self._vloga_tip_id

    @vloga_tip_id.setter
    def vloga_tip_id(self, vrednost):
        self._vloga_tip_id = vrednost

    def shrani_vsebina_oseba(self):
        """Shrani vsebina/oseba v bazo."""
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
                INSERT INTO vsebina_oseba (vloga, oseba_id, vsebina_id, vloga_tip_id)
                VALUES (?, ?, ?, ?)
            """, [self.vloga, self.oseba_id, self.vsebina_id, self.vloga_tip_id])
