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
        
        