import urllib.request
import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

#Importar links_ligamx.csv a listas para poder usarlos.
column_names = ["rows" , "tournament","year","links"]
df = pd.read_csv("../links_ligamx.csv", names = column_names)
tournament = df.tournament.tolist()
year = df.year.tolist()
links = df.links.tolist()
csvrows = df.rows.tolist()

for game in csvrows:
    link = links[game]
    URL = str(links[game])
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')

    #Y AQUI SE HACE CADA UNO, LOCAL Y AWAY POR SU CUENTA.
    # AHORA, TENGO QUE MODIFICAR LOCAL Y AWAY PARA QUE ESTEN EXTRAYENDO BIEN LOS DATOS Y NO STRINGS IRRACIONALES.



