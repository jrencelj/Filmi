import sqlite3 as dbapi


class Vloga_Tip:

    def __init__(self, sifra, naziv):
        self._sifra = sifra
        self._naziv = naziv

    def shrani_vloga_tip(self):
        '''Shrani tip vloge v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT INTO vloga_tip (sifra, naziv)
            VALUES (?, ?)
            """, [self._sifra, self._naziv])

    def pridobi_vloga_tip_id(self):
        '''Pridobi id tipa vloge iz baze'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM vloga_tip
                WHERE naziv=?
            """, [self._naziv])
            id = cursor.fetchone()[0]
            return id

    @property
    def sifra(self):
        return self._sifra

    @property
    def naziv(self):
        return self._naziv

    @sifra.setter
    def sifra(self, vrednost):
        self._sifra = vrednost

    @naziv.setter
    def naziv(self, vrednost):
        self._naziv = vrednost
