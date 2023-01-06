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

    def pridobi_zvrst_id(self):
        '''Pridobi id zvrsti iz baze'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM zvrst
                WHERE naziv_zvrsti=?
            """, [self._naziv_zvrsti])
            id = cursor.fetchone()[0]
            return id

    @property
    def naziv_zvrsti(self):
        return self._naziv_zvrsti

    @naziv_zvrsti.setter
    def naziv_zvrsti(self, vrednost):
        self._naziv_zvrsti = vrednost
