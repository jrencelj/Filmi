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


    # TODO Napiši get in set metode za atribute z @property za self._sifra in self._naziv
    