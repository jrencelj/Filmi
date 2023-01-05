import sqlite3 as dbapi
class Oseba:
    def __init__(self, ime_priimek, imdb_id_oseba, url_slika = None):
        self._ime_priimek = ime_priimek
        self._imdb_id_oseba = imdb_id_oseba
        self._url_slika = url_slika

    def shrani_oseba(self):
        '''Shrani osebo v bazo.'''
        conn = dbapi.connect('filmi.db') 
        with conn:
            conn.execute("""
            INSERT OR IGNORE INTO oseba (ime_priimek, url_slika, imdb_id_oseba)
            VALUES (?, ?, ?)
            """, [self._ime_priimek, self._url_slika, self._imdb_id_oseba])
        
    
    def pridobi_oseba():
        '''Pridobi osebo iz baze.'''
        # TODO
        pass