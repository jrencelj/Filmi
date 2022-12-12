from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.imdb.com/chart/top/"

def pridobiHtml(url):
    """Pridobi html vsebino spletne strani."""
    response = requests.get(url, headers = {"Accept-Language": "en-US,en;q=0.5"})
    return response.text

html_vsebina = pridobiHtml(url)

soup = BeautifulSoup(html_vsebina, "html.parser")

filmi = {'naslov' : [], 'leto' : []}

for td_znacka in soup.findAll("td", class_="titleColumn"):
    naslov = td_znacka.a.contents[0]
    leto = int(str(td_znacka.span.contents[0]).strip("()"))
    filmi["naslov"].append(str(naslov))
    filmi["leto"].append(leto)

df = pd.DataFrame(filmi)
df.to_csv("filmi.csv", sep = ';', index = False)