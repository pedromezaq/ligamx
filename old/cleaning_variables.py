import urllib.request
import requests
from bs4 import BeautifulSoup
import csv
import os
import re

#Erase previous CSV. Erase after testing ends.
os.remove("test.csv")


#Create CSV file and write header.
header = ['rows','tournament','year','count','local_dummy', 'minuto', 'name_link','numero','posicion','capitan','tarjeta','cambio']
with open('../test.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)


tournament = 0
year = 0




URL = "http://www.ligabbva.mx/cancha/informeArbitral/4729/eyJpZERpdmlzaW9uIjoiOSIsImlkVGVtcG9yYWRhIjoiNjIiLCJpZFRvcm5lbyI6IjEiLCJpZENsdWJsb2NhbCI6IjIwIiwiaWRDbHVidmlzaXRhIjoiMTEifQ==/informe-arbitral-uag-vs-pachuca-jornada6-estadio-3-de-marzo"
print(URL)
page = requests.get(URL)
subsoup = BeautifulSoup(page.content,'html.parser')
soup = BeautifulSoup(page.content,'html.parser')
# Sub soup to extract players' data.
#subsoup = soup.find("div", class_="jugadaJugada")

alineaciones = subsoup.select("div[class='alineacionMin gray']")
#alineaciones = subsoup.select("div[class='alineacionMin gray']")
#alineaciones = subsoup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['alineacionMin', 'gray'])
#print(alineaciones)
local = 0
count = 0
for alineacion in alineaciones:
    count = count + 1
    capitan = 0
    col_xs_12 = alineacion.find_all("li", class_="col-xs-12")
    #count = 5 son los cambios.
    if count != 5:
        for col in col_xs_12:
            #minuto.
            minuto = str(col.find("div",class_="col-xs-2 minutoGol"))
            minuto = " ".join(minuto.split())

            #name
            name = str(col.find("div", class_="jugador"))
            name = " ".join(name.split())
            html = BeautifulSoup(name,'html.parser')
            name = str([a['href'] for a in html.find_all('a')])[2:-2]
            name_link = "http://ligamx.net"+ str(name)

            #numero y capitan
            numero = str(col.find("strong", class_="numero"))
            numero = " ".join(numero.split())
            fullstring = numero
            substring = "capitan"
            if substring in fullstring:
                capitan= 1
            else:
                capitan = 0

            #posicion
            posicion = str(col.find("span", class_="posicion"))
            posicion = " ".join(posicion.split())

            # tarjetas
            tarjeta_string = str(col.find("div", class_="disp-table"))
            tarjeta_string = " ".join(tarjeta_string.split())
            #print(tarjeta_string)
            amarilla = "Tarjeta Amarilla"
            roja = "Tarjeta Roja"
            if amarilla in tarjeta_string:
                tarjeta = 1
            elif roja in tarjeta_string:
                tarjeta = 2
            else:
                tarjeta = 0

            #print(tarjeta)

            # replace with blanks.
            replace_strings = ['<div class="col-xs-2 minutoGol"><small>min</small><span>', '</span></div>','<strong class="numero">','</strong>', '<span class="posicion">','</span>','<span class="posicionJ guantes">','<span class="posicionJ capitan">']
            for replace in replace_strings:
                minuto = minuto.replace(replace,"")
                posicion=posicion.replace(replace,"")
                numero = numero.replace(replace,"")
            minuto = minuto.replace("'","").strip()
            numero = numero.replace("#","").strip()
            posicion =posicion.strip()
            name_link= name_link.strip()
            # print(name_link)
            # print(minuto)
            # print(posicion)
            # print(numero)
            entrasale = 0
            data = [row, tournament, year, count, local, minuto, name_link, numero, posicion, capitan,
                    tarjeta, entrasale]
            with open('../test.csv', 'a', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)


    elif count == 5:
        cambios = alineacion.select("li[class='col-xs-12 entraSale']")
        for cambio in cambios:
            rows = cambio.find_all("div", class_="row")
            for row in rows:
                # minuto
                minuto = str(row.find("div", class_="col-xs-2 minutoGol"))
                minuto = " ".join(minuto.split())

                # name_link
                name = str(row.find("div", class_="jugador"))
                name = " ".join(name.split())
                html = BeautifulSoup(name, 'html.parser')
                name = str([a['href'] for a in html.find_all('a')])[2:-2]
                name_link = "http://ligamx.net" + str(name)

                # numero y capitan
                numero = str(row.find("strong", class_="numero"))
                numero = " ".join(numero.split())
                fullstring = numero
                substring = "capitan"
                if substring in fullstring:
                    capitan = 1
                else:
                    capitan = 0

                # capitan
                posicion = str(row.find("span", class_="posicion"))
                posicion = " ".join(posicion.split())

                # entrasale
                entrasale_string = str(row.find("div", class_="disp-table"))
                entrasale_string = " ".join(entrasale_string.split())
                entra = "Entra"
                sale = "Sale"
                if entra in entrasale_string:
                    entrasale = 1
                elif sale in tarjeta_string:
                    entrasale = 2
                else:
                    entrasale = 0
                print(entrasale)
                # replace with blanks.
                replace_strings = ['<div class="col-xs-2 minutoGol"><small>min</small><span>', '</span></div>',
                                   '<strong class="numero">', '</strong>', '<span class="posicion">', '</span>',
                                   '<span class="posicionJ guantes">', '<span class="posicionJ capitan">']
                for replace in replace_strings:
                    minuto = minuto.replace(replace, "")
                    posicion = posicion.replace(replace, "")
                    numero = numero.replace(replace, "")
                minuto = minuto.replace("'", "").strip()
                numero = numero.replace("#", "").strip()
                posicion = posicion.strip()
                name_link = name_link.strip()
                # print(name_link)
                # print(minuto)
                # print(posicion)
                # print(numero)
                capitan = 4
                tarjeta= 4
                data = [row, tournament, year, count, local, minuto, name_link, numero, posicion, capitan,
                        tarjeta, entrasale]
                with open('../test.csv', 'a', encoding='UTF-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
