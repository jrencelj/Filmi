import requests
from datetime import datetime

class Bralnik:

    @staticmethod
    def pridobi_html(url):
        """Pridobi html vsebino spletne strani."""
        odziv = requests.get(url, headers = {
            'Accept-Language': 'en-US,en;q=0.5', 
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15'
            })
        return odziv.text

    @staticmethod
    def preoblikuj_v_ime(ime_vsebine):
        '''Prejme ime vsebine. Preoblikuje ime vsebine v ime datoeke.'''
        return ime_vsebine.lower().replace(': ', '_').replace(' ', '_').replace('\'', '_').replace('/', '_')

    @staticmethod
    def v_tip_datum(datum):
        '''Preoblikuje niz v objekt razreda datum.'''
        meseci = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12

        }
        if datum == 'N/A': return None
        dan, mesec, leto = datum.split()
        return datetime(int(leto), meseci[mesec], int(dan))

    @staticmethod
    def v_tip_datum_tri_crke(datum):
        '''Preoblikuje niz v objekt razreda datum.'''
        meseci = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12

        }
        if datum == 'N/A': return None
        dan, mesec, leto = datum.split()
        return datetime(int(leto), meseci[mesec], int(dan))

if __name__ == '__main__':
    print(Bralnik.v_tip_datum('24 December 2009'))