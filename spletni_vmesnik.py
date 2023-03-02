import bottle
from film import Film
from serija import Serija
from vsebina import Vsebina
from uporabnik import Uporabnik
from uporabnik_tip import Uporabnik_Tip
import hashlib
import time
from komentar import Komentar
from vsebina_komentar import Vsebina_Komentar
from oseba import Oseba


def hash_geslo(geslo):
    tekst = geslo.encode("utf-8")
    d = hashlib.sha256(tekst)
    hash = d.hexdigest()
    return hash


def pridobi_uporabnika():
    """Kdo je uporabnik."""
    uporabnisko_ime = bottle.request.get_cookie(
        'uporabnisko_ime', secret='skrivnost')
    if uporabnisko_ime is not None:
        return uporabnisko_ime
    else:
        return None


@bottle.route('/<filename>.css')
def stylesheets(filename):
    return bottle.static_file(f'{filename}.css', root='static')


@bottle.route('/static/<filename>.jpeg')
def jpeg(filename):
    return bottle.static_file(f'{filename}.jpeg', root='static')


@bottle.route('/static/default_avatar.png')
def default_avatar():
    return bottle.static_file('default_avatar.png', root='static')


@bottle.route("/")
def glavna_stran():
    return bottle.template('index.html', root='Projekt', uporabnisko_ime=pridobi_uporabnika())


@bottle.post('/do_prijava')
def do_prijava():
    uporabnisko_ime = bottle.request.forms.getunicode("username")
    geslo = bottle.request.forms.getunicode("pass")
    if Uporabnik.je_uporabnik(uporabnisko_ime):
        uporabnik = Uporabnik.pridobi_uporabnika_po_username(uporabnisko_ime)
        if hash_geslo(geslo + uporabnik.sol) == uporabnik.geslo:
            bottle.response.set_cookie(
                "uporabnisko_ime", uporabnisko_ime, path='/', secret='skrivnost')
            bottle.redirect('/')
        else:
            return bottle.template('index.html', uporabnisko_ime=pridobi_uporabnika())
    else:
        return bottle.template('index.html', uporabnisko_ime=pridobi_uporabnika())


@bottle.route("/odjava")
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime')
    bottle.redirect('/')


@bottle.post('/do_registracija')
def do_registracija():
    email = bottle.request.forms.getunicode("email")
    uporabnisko_ime = bottle.request.forms.getunicode("username")
    pass1 = bottle.request.forms.getunicode("pass1")
    pass2 = bottle.request.forms.getunicode("pass2")
    if pass1 == pass2 and not Uporabnik.je_uporabnik(uporabnisko_ime) and not Uporabnik.email_obstaja(email):
        sol = "sol"
        geslo = hash_geslo(pass1 + sol)
        datum_rojstva = bottle.request.forms.getunicode("bday")
        uporabnik = Uporabnik(None, uporabnisko_ime, email, datum_rojstva,
                              geslo, sol, Uporabnik_Tip("U", "uporabnik", None))
        uporabnik.shrani_uporabnik()
        return bottle.template('index.html', uporabnisko_ime=pridobi_uporabnika())
    else:
        return bottle.template('index.html', uporabnisko_ime=pridobi_uporabnika(), napake='Gesli se ne ujemata.')


@bottle.route("/registracija")
def registracija():
    return bottle.template('registracija.html')


@bottle.route("/filmi/<stran:int>")
def filmi(stran):
    filmi = Film.pridobi_vse_filme()
    return bottle.template('filmi.html', filmi=filmi, stran=stran, uporabnisko_ime=pridobi_uporabnika())


@bottle.route("/generator_film")
def generator_film():
    filmi = Film.pridobi_vse_filme()
    predlogi = []
    return bottle.template('generator_film.html', filmi=filmi, predlogi=predlogi, uporabnisko_ime=pridobi_uporabnika())


@bottle.route("/generator_serija")
def generator_serija():
    serije = Serija.pridobi_vse_serije()
    predlogi = []
    return bottle.template('generator_serija.html', serije=serije, predlogi=predlogi, uporabnisko_ime=pridobi_uporabnika())


@bottle.post("/generator_serija")
def do_predlaga_serija():
    serija1 = bottle.request.forms.getunicode("izberi_serija1")
    serija2 = bottle.request.forms.getunicode("izberi_serija2")
    serija3 = bottle.request.forms.getunicode("izberi_serija3")
    serije = Serija.pridobi_vse_serije()
    predlogi = Serija.pridobi_predloge_za_serijo(serija1, serija2, serija3)
    return bottle.template("generator_serija", serije=serije, predlogi=predlogi, uporabnisko_ime=pridobi_uporabnika())


@bottle.post("/generator_film")
def do_predlaga_filmi():
    film1 = bottle.request.forms.getunicode("izberi_film1")
    film2 = bottle.request.forms.getunicode("izberi_film2")
    film3 = bottle.request.forms.getunicode("izberi_film3")
    filmi = Film.pridobi_vse_filme()
    predlogi = Film.pridobi_predloge_za_film(film1, film2, film3)
    return bottle.template("generator_film", filmi=filmi, predlogi=predlogi, uporabnisko_ime=pridobi_uporabnika())


@bottle.route("/serije/<stran:int>")
def serije(stran):
    serije = Serija.pridobi_vse_serije()
    return bottle.template('serije.html', serije=serije, stran=stran, uporabnisko_ime=pridobi_uporabnika())


@bottle.post("/filmi/podrobno/<id:int>")
def do_komentar(id):
    ocena = bottle.request.forms.getunicode("ocena")
    besedilo_komentar = bottle.request.forms.getunicode("comment")
    cas = time.time()
    uporabnik_id = Uporabnik.pridobi_uporabnika_po_username(
        pridobi_uporabnika()).id
    komentar = Komentar(None, ocena, cas, None,
                        besedilo_komentar, uporabnik_id)
    komentar.shrani_komentar()
    id_komentar = Komentar.pridobi_id_komentar(
        uporabnik_id, besedilo_komentar, cas, ocena)
    Vsebina_Komentar(None, id, id_komentar).shrani_vsebina_komentar()
    bottle.redirect(f'/filmi/podrobno/{id}')


@bottle.get("/filmi/podrobno/<id:int>")
def podrobno_film(id):
    film = Film.pridobi_film_z_id(id)
    komentarji_filma = Film.pridobi_komentarje_po_id_film(id)
    reziserji = Vsebina.pridobi_reziserje_za_vsebino(id)
    igralci = Vsebina.pridobi_igralce_za_vsebino(id)
    kinoteke = Vsebina.pridobi_kinoteke_za_vsebino(id)
    vneseni_komentarji = Komentar.pridobi_komentarje_za_vsebino(id)
    return bottle.template('podrobno_film.html', film=film, komentarji_filma=komentarji_filma, reziserji=reziserji, igralci=igralci, kinoteke=kinoteke,
                           uporabnisko_ime=pridobi_uporabnika(), vneseni_komentarji=vneseni_komentarji)


@bottle.post("/serije/podrobno/<id:int>")
def do_komentar(id):
    ocena = bottle.request.forms.getunicode("ocena")
    besedilo_komentar = bottle.request.forms.getunicode("comment")
    cas = time.time()
    uporabnik_id = Uporabnik.pridobi_uporabnika_po_username(
        pridobi_uporabnika()).id
    komentar = Komentar(None, ocena, cas, None,
                        besedilo_komentar, uporabnik_id)
    komentar.shrani_komentar()
    id_komentar = Komentar.pridobi_id_komentar(
        uporabnik_id, besedilo_komentar, cas, ocena)
    Vsebina_Komentar(None, id, id_komentar).shrani_vsebina_komentar()
    bottle.redirect(f'/serije/podrobno/{id}')


@bottle.get("/serije/podrobno/<id:int>")
def podrobno_serija(id):
    serija = Serija.pridobi_serijo_z_id(id)
    komentarji_serije = Serija.pridobi_komentarje_po_id_serija(id)
    reziserji = Vsebina.pridobi_reziserje_za_vsebino(id)
    igralci = Vsebina.pridobi_igralce_za_vsebino(id)
    kinoteke = Vsebina.pridobi_kinoteke_za_vsebino(id)
    vneseni_komentarji = Komentar.pridobi_komentarje_za_vsebino(id)
    return bottle.template('podrobno_serija.html', serija=serija, komentarji_serije=komentarji_serije, reziserji=reziserji, igralci=igralci,
                           kinoteke=kinoteke, uporabnisko_ime=pridobi_uporabnika(), vneseni_komentarji=vneseni_komentarji)


@bottle.route("/oseba/<id:int>")
def oseba(id):
    podatki_oseba = Oseba.pridobi_oseba_po_id(id)
    vsebine_osebe = Vsebina.pridobi_vsebine_za_igralca(id)
    return bottle.template('oseba.html', podatki_oseba=podatki_oseba, vsebine_osebe=vsebine_osebe, uporabnisko_ime=pridobi_uporabnika())


# _____________________________________
@bottle.route("/iskanje_filmi/<stran:int>/<niz>")
def iskanje_filmi(stran, niz="main"):
    filmi = Film.pridobi_vse_filme()
    print(niz)
    if niz == 'main' or niz == "":
        najdeni = Film.pridobi_vse_filme()
    else:
        najdeni = Film.pridobi_zeljene_filme(niz)
    return bottle.template('iskanje_filmi.html', filmi=filmi, najdeni=najdeni, stran=stran, niz=niz, uporabnisko_ime=pridobi_uporabnika())


@bottle.post("/iskanje_filmi/<stran:int>")
def iskanje_filmi2(stran):
    filmi = Film.pridobi_vse_filme()
    niz = bottle.request.forms.getunicode('iskani_filmi')
    najdeni = Film.pridobi_zeljene_filme(niz)
    return bottle.template('iskanje_filmi.html', filmi=filmi, najdeni=najdeni, stran=stran, niz=niz, uporabnisko_ime=pridobi_uporabnika())


@bottle.route("/iskanje_serije/<stran:int>/<niz>")
def iskanje_serije(stran, niz="main"):
    serije = Serija.pridobi_vse_serije()
    if niz == 'main' or niz == "":
        najdene = Serija.pridobi_vse_serije()
    else:
        najdene = Serija.pridobi_zeljene_serije(niz)
    return bottle.template('iskanje_serije.html', serije=serije, najdene=najdene, stran=stran, niz=niz, uporabnisko_ime=pridobi_uporabnika())


@bottle.post("/iskanje_serije/<stran:int>")
def iskanje_serije2(stran):
    serije = Serija.pridobi_vse_serije()
    niz = bottle.request.forms.getunicode('iskane_serije')
    najdene = Serija.pridobi_zeljene_serije(niz)
    return bottle.template('iskanje_serije.html', serije=serije, najdene=najdene, stran=stran, niz=niz, uporabnisko_ime=pridobi_uporabnika())

# _____________________________________


bottle.run(debug=True, reloader=True)
