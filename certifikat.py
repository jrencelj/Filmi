import sqlite3 as dbapi


class Certifikat:
    def __init__(self, sifra):
        self._sifra = sifra

    def shrani_certifikat(self):
        '''Shrani certifikat v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT OR IGNORE INTO certifikat (sifra)
            VALUES (?)
            """, [self._sifra])

    def pridobi_certifikat_id(self):
        '''Pridobi id certifikata iz baze.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM certifikat
                WHERE sifra=?
            """, [self._sifra])
            id = cursor.fetchone()[0]
            return id

    @property
    def sifra(self):
        return self._sifra

    @property.setter
    def sifra(self, vrednost):
        self._sifra = vrednost

    @staticmethod
    def pridobi_certifikat_po_id(id):
        '''Pridobi pripadajočo šifro glede na id in vrne certifikat.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT sifra FROM certifikat
                WHERE id=?
            """, [id])
            sifra = cursor.fetchone()[0]
            return Certifikat(sifra)
