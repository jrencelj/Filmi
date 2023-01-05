import sqlite3 as dbapi


class Oseba:
    def __init__(self, ime_priimek, imdb_id_oseba, url_slika=None):
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

    # TODO pridobi_oseba_id(self), WHERE po 'imdb_id_oseba'

    def pridobi_oseba():
        '''Pridobi osebo iz baze.'''
        # TODO
        pass

    @property
    def ime_priimek(self):
        return self._ime_priimek

    @property
    def imdb_id_oseba(self):
        return self._imdb_id_oseba

    @property
    def url_slika(self):
        return self._url_slika

    @ime_priimek.setter
    def ime_priimek(self, vrednost):
        self._ime_priimek = vrednost

    @imdb_id_oseba.setter
    def imdb_id_oseba(self, vrednost):
        self._imdb_id_oseba = vrednost

    @url_slika.setter
    def url_slika(self, vrednost):
        self._url_slika = vrednost
