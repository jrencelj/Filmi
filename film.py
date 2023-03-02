from certifikat import Certifikat
from vsebina_tip import Vsebina_Tip
from vsebina import Vsebina
from drzava import Drzava
import sqlite3 as dbapi
from bralnik import Bralnik
from vsebina_tip import Vsebina_Tip
from komentarIMDB import KomentarIMDB


class Film(Vsebina):
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

    @property
    def certifikat(self):
        return self._certifikat

    @property
    def leto_izida(self):
        return self._leto_izida

    @certifikat.setter
    def certifikat(self, vrednost):
        self._certifikat = vrednost

    @leto_izida.setter
    def leto_izida(self, vrednost):
        self._leto_izida = vrednost


    def shrani_film(self):
        '''Shrani film v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT INTO vsebina (naslov, dolzina, leto_izida, url_slika, imdb_id_vsebina, opis, datum_prvega_predvajanje, certifikat_id,
                            vsebina_tip_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [super().naslov, super().dolzina, self._leto_izida, super().url_slika, super().imdb_id_vsebina,
                  super().opis, Bralnik.v_tip_datum_tri_crke(
                      self._datum_prvega_predvajanja), self._certifikat.pridobi_certifikat_id(),
                  super().vsebina_tip.pridobi_vsebina_tip_id()])

    @staticmethod
    def pridobi_film_z_id(id):
        '''Pridobi podatke za film za danim id-jem.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
            SELECT * FROM vsebina WHERE id = ?
            """, [id])
            podatek = cursor.fetchone()
        return Film(podatek[0], podatek[1], podatek[2], podatek[4], podatek[5], podatek[6], podatek[7], Vsebina_Tip.pridobi_vsebina_tip_po_id(podatek[11]),
                    podatek[3], Certifikat.pridobi_certifikat_po_id(podatek[10]))

    @staticmethod
    def pridobi_vse_filme():
        """Pridobi vse filme iz baze in jih vrne v seznama."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
            SELECT * FROM vsebina WHERE vsebina_tip_id = 1
            """)
            podatki = list(cursor.fetchall())
            return [
                Film(podatek[0], podatek[1], podatek[2], podatek[4], podatek[5], podatek[6], podatek[7],
                     Vsebina_Tip.pridobi_vsebina_tip_po_id(podatek[11]), podatek[3], Certifikat.pridobi_certifikat_po_id(podatek[10]))
                for podatek in podatki
            ]

    # __________________________________________
    @staticmethod
    def pridobi_zeljene_filme(predlog):
        """Pridobi zeljene filme iz baze in jih vrne v seznama."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
            SELECT * FROM vsebina WHERE vsebina_tip_id = 1 and naslov like ?
            """, ["%"+predlog+"%"])
            podatki = list(cursor.fetchall())
            return [
                Vsebina(podatek[0], podatek[1], podatek[2], podatek[4],
                        podatek[5], podatek[6], podatek[7], podatek[11])
                for podatek in podatki
            ]
    # ______________________________________________

    @staticmethod
    def pridobi_predloge_za_film(naslov1, naslov2, naslov3):
        """Pridobi predloge za film glede na všečne filme."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""SELECT DISTINCT t1.* FROM vsebina AS t1 INNER JOIN vsebina_imdb_komentar AS t2 ON t1.id = t2.vsebina_id INNER JOIN imdb_komentar AS t3 ON t2.imdb_komentar_id = t3.id
            WHERE t3.imdb_id_uporabnik IN (SELECT t3.imdb_id_uporabnik FROM vsebina AS t1 INNER JOIN vsebina_imdb_komentar AS t2 ON t1.id = t2.vsebina_id INNER JOIN imdb_komentar AS t3 ON t2.imdb_komentar_id = t3.id
            WHERE (t1.naslov=? OR t1.naslov = ? OR t1.naslov=?) AND t3.ocena = 10) AND t3.ocena = 10 AND vsebina_tip_id = 1 AND t1.naslov NOT IN (?,?,?)  GROUP BY t1.naslov HAVING COUNT(*) > 150;
            """, [naslov1, naslov2, naslov3, naslov1, naslov2, naslov3])
            podatki = list(cursor.fetchall())
            return [
                Vsebina(podatek[0], podatek[1], podatek[2], podatek[4], podatek[5], podatek[6], podatek[7], podatek[11])
                for podatek in podatki
            ]

    @staticmethod
    def pridobi_komentarje_po_id_film(id):
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
            SELECT t3.* FROM vsebina AS t1 INNER JOIN vsebina_imdb_komentar AS t2 ON t1.id = t2.vsebina_id
            INNER JOIN imdb_komentar AS t3 ON t2.imdb_komentar_id = t3.id
            WHERE t1.id=?
            LIMIT 3
            """, [id])
            podatki = cursor.fetchall()
        return [
            KomentarIMDB(podatek[0], podatek[1], podatek[2], podatek[3], podatek[4], podatek[5], podatek[6], podatek[7], podatek[8],
                         podatek[9], podatek[10])
            for podatek in podatki
        ]