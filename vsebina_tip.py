import sqlite3 as dbapi


class Vsebina_Tip:

    def __init__(self, naziv):
        self._naziv = naziv

    def shrani_vsebina_tip(self):
        '''Shrani tip vsebine v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT INTO vsebina_tip (naziv)
            VALUES (?)
            """, [self._naziv])

    def pridobi_vsebina_tip_id(self):
        '''Pridobi id tipa vsebine iz baze.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM vsebina_tip
                WHERE naziv=?
            """, [self._naziv])
            id = cursor.fetchone()[0]
            return id

    @staticmethod
    def pridobi_vsebina_tip_po_id(id):
        '''Pridobi pripadajoč tip vsebine glede na id in vrne certifikat.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT naziv FROM vsebina_tip
                WHERE id=?
            """, [id])
            naziv = cursor.fetchone()[0]
            return Vsebina_Tip(naziv)

    @property
    def naziv(self):
        return self._naziv

    @property.setter
    def naziv(self, vrednost):
        self._naziv = vrednost
