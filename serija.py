from vsebina import Vsebina
import sqlite3 as dbapi
from bralnik import Bralnik

class Serija(Vsebina):
    def __init__(self, naslov, dolzina, imdb_id, opis, datum_prvega_predvajanja, leto_izida,
                 certifikat, vsebina_tip):
        super()._naslov = naslov
        super()._dolzina = dolzina
        # TODO

    def shrani_serija(self):
        '''Shrani serijo v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT INTO vsebina (naslov, dolzina, leto_izida, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanje, certifikat_id,
                            vsebina_tip_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [super()._naslov, super().get_dolzina(), self._leto_izida, super().get_url_slika(), super().get_imdb_id_vsebina(),
                  super().get_opis(), Bralnik.v_tip_datum_tri_crke(
                      self._datum_prvega_predvajanja), self._certifikat.pridobi_certifikat_id(),
                  super().get_vsebina_tip().pridobi_vsebina_tip_id()])


    @property.setter
    def imdb_id(self, vrednost):
        self._imdb_id = vrednost

    @property
    def imdb_id(self):
        return self._imdb_id

    @property.setter
    def imdb_id(self, vrednost):
        self._imdb_id = vrednost

    @property
    def leto_izida(self):
        return self._leto_izida

    @property.setter
    def leto_izida(self, vrednost):
        self._leto_izida = vrednost

    @property
    def certifikat(self):
        return self._certifikat

    @property.setter
    def certifikat(self, vrednost):
        self._certifikat = vrednost
