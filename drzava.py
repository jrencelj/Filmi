import sqlite3 as dbapi


class Drzava:

    def __init__(self, drzava_ime):
        self._drzava_ime = drzava_ime

    def shrani_drzava(self):
        '''Shrani državo v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT OR IGNORE INTO drzava (drzava_ime)
            VALUES (?)
            """, [self._drzava_ime])

    @staticmethod
    def pridobi_drzava_id(drzava_ime):
        '''Pridobi id države iz baze.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM drzava
                WHERE drzava_ime=?
            """, [drzava_ime])
            podatki = cursor.fetchone()
            return Drzava(podatki[0])

    @property
    def drzava_ime(self):
        return self._drzava_ime

    @drzava_ime.setter
    def drzava_ime(self, vrednost):
        self._drzava_ime = vrednost
