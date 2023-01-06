import sqlite3 as dbapi


class Uporabnik_Tip:
    def __init__(self, sifra, naziv, opis):
        self._sifra = sifra
        self._naziv = naziv
        self._opis = opis

    def shrani_uporabnik_tip(self):
        '''Shrani uporabnik tip v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT INTO uporabnik_tip (sifra, naziv, opis)
            VALUES (?, ?, ?)
            """, [self._sifra, self._naziv, self._opis])

    def pridobi_uporabnik_tip_id(self):
        '''Pridobi id uporabniškega tipa iz baze'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM uporabnik_tip
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

    @property
    def opis(self):
        return self._opis

    @sifra.setter
    def sifra(self, vrednost):
        self._sifra = vrednost

    @naziv.setter
    def naziv(self, vrednost):
        self._naziv = vrednost

    @opis.setter
    def opis(self, vrednost):
        self._opis = vrednost
