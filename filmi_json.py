import json
from omdb import KEY
import requests
import pandas as pd

vsebina = pd.read_csv("filmi.csv", sep = ';', header = 0, names = ("naslov", "leto"))

filmi = dict()

for indeks, vrstica in vsebina.iterrows():
    naslov = vrstica["naslov"]
    leto = vrstica["leto"]
    json_film = requests.get(f"http://www.omdbapi.com/?apikey={KEY}&t={naslov.replace(' ', '+')}&y={leto}&plot=full").json()
    filmi[f"{naslov}"] = json_film

with open("filmi.json", "w") as f:
    json.dump(filmi, f)