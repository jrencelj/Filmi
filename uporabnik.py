from uporabnik_tip import Uporabnik_Tip
import sqlite3 as dbapi


class Uporabnik:
    def __init__(self, id, uporabnisko_ime, e_naslov, datum_rojstva, geslo, sol, uporabnik_tip):
        self._id = id
        self._uporabnisko_ime = uporabnisko_ime
        self._e_naslov = e_naslov
        self._datum_rojstva = datum_rojstva
        self._geslo = geslo
        self._sol = sol
        self._uporabnik_tip = uporabnik_tip

    def shrani_uporabnik(self):
        '''Shrani uporabnika v bazo.'''
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
                INSERT INTO uporabnik (uporabnisko_ime, e_naslov, datum_rojstva, geslo, sol, uporabnik_tip_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [self.uporabnisko_ime, self.e_naslov, self.datum_rojstva, self.geslo, self.sol, self.uporabnik_tip.pridobi_uporabnik_tip_id()])
        pass

    def pridobi_uporabnik_id(self):
        '''Pridobi id uporabnika iz baze'''
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT id FROM uporabnik
                WHERE uporabnisko_ime=?
            """, [self._uporabnisko_ime])
            id = cursor.fetchone()[0]
            return id
    
    @staticmethod
    def pridobi_uporabnika_po_username(username):
        """Pridobi uporabnika po username."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT * FROM uporabnik WHERE uporabnisko_ime=?
            """, [username])
            podatek = cursor.fetchone()
        return Uporabnik(podatek[0], podatek[1], podatek[2], podatek[3], podatek[4], podatek[5], podatek[6])
    
    @staticmethod
    def je_uporabnik(username):
        """Preveri ali uporabnik že obstaja."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT * FROM uporabnik WHERE uporabnisko_ime=?
            """, [username])
            podatek = cursor.fetchone()
            if podatek:
                return True
        return False
    
    @staticmethod
    def email_obstaja(email):
        """Preveri ali email že obstaja."""
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT e_naslov FROM uporabnik WHERE e_naslov=?
            """, [email])
            podatek = cursor.fetchone()
            if podatek:
                return True
        return False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, vrednost):
        self._id = vrednost

    @property
    def sol(self):
        return self._sol

    @sol.setter
    def sol(self, vrednost):
        self._sol = vrednost

    @property
    def uporabnisko_ime(self):
        return self._uporabnisko_ime

    @property
    def e_naslov(self):
        return self._e_naslov

    @property
    def datum_rojstva(self):
        return self._datum_rojstva

    @property
    def geslo(self):
        return self._geslo

    @property
    def uporabnik_tip(self):
        return self._uporabnik_tip

    @uporabnisko_ime.setter
    def uporabnisko_ime(self, vrednost):
        self._uporabnisko_ime = vrednost

    @e_naslov.setter
    def e_naslov(self, vrednost):
        self._e_naslov = vrednost

    @datum_rojstva.setter
    def datum_rojstva(self, vrednost):
        self._datum_rojstva = vrednost

    @geslo.setter
    def geslo(self, vrednost):
        self._geslo = vrednost

    @uporabnik_tip.setter
    def uporabnik_tip(self, vrednost):
        self._uporabnik_tip = vrednost
