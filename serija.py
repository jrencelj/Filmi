from vsebina import Vsebina
import sqlite3 as dbapi
from bralnik import Bralnik
from certifikat import Certifikat
from vsebina_tip import Vsebina_Tip

class Serija(Vsebina):

    def __init__(self, id, naslov, dolzina, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanja, vsebina_tip, leto_izida,
                 certifikat):
        if not isinstance(certifikat, Certifikat):
            raise Exception(f'{certifikat} ni objekt razreda Certifikat!')
        else:
            self._certifikat = certifikat
        if not isinstance(leto_izida, int):
            raise Exception(f'{leto_izida} ni objekt razreda int!')
        else:
            self._leto_izida = leto_izida
        super().__init__(id, naslov, dolzina, url_slika, imdb_id_vsebina,
                         opis, datum_prvega_predvajanja, vsebina_tip)

        #TODO

    @property
    def leto_izida(self):
        return self._leto_izida

    @leto_izida.setter
    def leto_izida(self, vrednost):
        self._leto_izida = vrednost

    @property
    def certifikat(self):
        return self._certifikat

    @certifikat.setter
    def certifikat(self, vrednost):
        self._certifikat = vrednost

    def shrani_serija(self):
        '''Shrani serijo v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT INTO vsebina (naslov, dolzina, leto_izida, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanje, certifikat_id,
                            vsebina_tip_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [self.naslov, self.dolzina, self.leto_izida, self.url_slika, self.imdb_id_vsebina,
                  self.opis, Bralnik.v_tip_datum_tri_crke(
                      self.datum_prvega_predvajanja), self.certifikat.pridobi_certifikat_id(),
                  self.vsebina_tip.pridobi_vsebina_tip_id()])

    @staticmethod
    def pridobi_serijo_z_id(id):
        '''Pridobi podatke za serijo z danim id-jem.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
            SELECT * FROM vsebina WHERE id = ?
            """, [id])
            podatek = cursor.fetchone()
        return Serija(podatek[0], podatek[1], podatek[2], podatek[4], podatek[5], podatek[6], podatek[7], Vsebina_Tip.pridobi_vsebina_tip_po_id(podatek[11]),
                    podatek[3], Certifikat.pridobi_certifikat_po_id(podatek[10]))

    @staticmethod
    def pridobi_vse_serije():
        '''Pridobi vse filme iz baze in jih vrne v seznama.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
            SELECT * FROM vsebina WHERE vsebina_tip_id = 2
            """)
            podatki = list(cursor.fetchall())
            return [
                Serija(podatek[0], podatek[1], podatek[2], podatek[4], podatek[5], podatek[6], podatek[7],
                     Vsebina_Tip.pridobi_vsebina_tip_po_id(podatek[11]), podatek[3], Certifikat.pridobi_certifikat_po_id(podatek[10]))
                for podatek in podatki
            ]