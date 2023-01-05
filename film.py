from certifikat import Certifikat
from vsebina_tip import Vsebina_Tip
from vsebina import Vsebina
from drzava import Drzava
import sqlite3 as dbapi
from bralnik import Bralnik
from vsebina_tip import Vsebina_Tip

class Film(Vsebina):
    def __init__(self, naslov, dolzina, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanja, vsebina_tip, leto_izida,
                certifikat):
        if not isinstance(certifikat, Certifikat):
            raise Exception(f'{certifikat} ni objekt razreda Certifikat')
        else:
            self._certifikat = certifikat
        if not isinstance(leto_izida, int):
            raise Exception(f'{leto_izida} ni objekt razreda int')
        else:
            self._leto_izida = leto_izida
        super().__init__(naslov, dolzina, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanja, vsebina_tip)

    def shrani_film(self):
        '''Shrani film v bazo.'''
        conn = dbapi.connect('filmi.db') 
        with conn:
            conn.execute("""
            INSERT INTO vsebina (naslov, dolzina, leto_izida, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanje, certifikat_id,
                            vsebina_tip_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [super().get_naslov(), super().get_dolzina(), self._leto_izida, super().get_url_slika(), super().get_imdb_id_vsebina(),
                    super().get_opis(), Bralnik.v_tip_datum_tri_crke(self._datum_prvega_predvajanja), self._certifikat.pridobi_certifikat_id(), 
                    super().get_vsebina_tip().pridobi_vsebina_tip_id()])

    @staticmethod
    def pridobi_vse_filme():
        '''Pridobi vse filme iz baze in jih vrne v seznama.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
            SELECT * FROM vsebina WHERE vsebina_tip_id = 1
            """)
            podatki = list(cursor.fetchall())
            return [
                Film(podatek[1], podatek[2], podatek[4], podatek[5], podatek[6], podatek[7], 
                    Vsebina_Tip.pridobi_vsebina_tip_po_id(podatek[11]), podatek[3], Certifikat.pridobi_certifikat_po_id(podatek[10]))
                for podatek in podatki
            ]