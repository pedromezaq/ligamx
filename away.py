import urllib.request
import requests
from bs4 import BeautifulSoup
import csv
import os

with open("links.csv") as file_name:
    file_read = csv.reader(file_name)
    links = list(file_read)
#print(links)
#Erase previous CSV. Erase after testing ends.
os.remove("away.csv")

#Create CSV file and write header.
header = ['count','local_dummy', 'minuto', 'name','numero','posicion']
with open('away.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)


for link in links:
    URL = str(link)[2:-2]
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')

    # Sub soup to extract players' data.
    subsoup = soup.find("div",class_="jugadaJugada")
    alineaciones = subsoup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['alineacionMin' , 'gray'])
    local = 0
    count = 0
    for alineacion in alineaciones:
        count = count +1
        col_xs_12 = alineacion.find_all("li",class_="col-xs-12")
        if count!=5 :
            for col in col_xs_12:
                minuto = col.find("div", class_="col-xs-2 minutoGol")
                name = col.find("div", class_="jugador")
                numero = col.find("strong", class_="numero")
                posicion = col.find("span", class_="posicion")
                data = [count,local, minuto, name, numero, posicion]
                with open('away.csv', 'a', encoding='UTF-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
        elif count==5:
            print("cambios")

    count=5
    cambios = subsoup.find_all("li",class_="col-xs-12 entraSale")
    for cambio in cambios:
        rows = cambio.find_all("div",class_="row")
        for row in rows:
            minuto = row.find("div", class_="col-xs-2 minutoGol")
            name = row.find("div", class_="jugador")
            numero = row.find("strong", class_="numero")
            posicion = row.find("span", class_="posicion")
            data = [count,local, minuto, name, numero, posicion]
            with open('away.csv', 'a', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)