import sqlite3 as dbapi


class Zvrst:

    def __init__(self, naziv_zvrsti):
        self._naziv_zvrsti = naziv_zvrsti

    def shrani_zvrst(self):
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT OR IGNORE INTO zvrst (naziv_zvrsti)
            VALUES (?)
            """, [self._naziv_zvrsti])

    @property
    def naziv_zvrsti(self):
        return self._naziv_zvrsti

    @naziv_zvrsti.setter
    def naziv_zvrsti(self, vrednost):
        self._naziv_zvrsti = vrednost
