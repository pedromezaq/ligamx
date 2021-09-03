import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import csv
import pandas as pd
import logging
import multiprocessing as mp
import os.path
logging.basicConfig(level=logging.DEBUG)

# Importar links.csv a listas para poder usarlos.
column_names = ["rows", "tournament", "year", "links"]
df = pd.read_csv("links.csv", names=column_names)
tournaments = df.tournament.tolist()
years = df.year.tolist()
links = df.links.tolist()
csvrows = df.rows.tolist()

# Erase previous CSV.
if os.path.isfile('data.csv'):
    os.remove("data.csv")
else:
    print("Create file.")
# Create CSV file and write header.
header = ['game', 'tournament', 'year', 'count', 'local_dummy', 'minuto', 'name_link', 'numero', 'posicion',
          'capitan', 'tarjeta', 'cambio']
with open('data.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
print(len(csvrows))


def funcion(game):
    print(game)
    tournament = str(tournaments[game])
    year = str(years[game])
    url = str(links[game])
    logging.basicConfig(level=logging.DEBUG)

    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))

    page = s.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    alineaciones = soup.select("div[class='alineacionMin gray']")
    local = 0
    count = 0
    for alineacion in alineaciones:
        count = count + 1
        col_xs_12 = alineacion.find_all("li", class_="col-xs-12")
        # count = 5 son los cambios.
        if count != 5:
            for col in col_xs_12:
                # minuto.
                minuto = str(col.find("div", class_="col-xs-2 minutoGol"))
                minuto = " ".join(minuto.split())

                # name
                name = str(col.find("div", class_="jugador"))
                name = " ".join(name.split())
                html = BeautifulSoup(name, 'html.parser')
                name = str([a['href'] for a in html.find_all('a')])[2:-2]
                name_link = "http://ligamx.net" + str(name)

                # numero y capitan
                numero = str(col.find("strong", class_="numero"))
                numero = " ".join(numero.split())
                fullstring = numero
                substring = "capitan"
                if substring in fullstring:
                    capitan = 1
                else:
                    capitan = 0

                # posicion
                posicion = str(col.find("span", class_="posicion"))
                posicion = " ".join(posicion.split())

                # tarjetas
                tarjeta_string = str(col.find("div", class_="disp-table"))
                tarjeta_string = " ".join(tarjeta_string.split())
                # print(tarjeta_string)
                amarilla = "Tarjeta Amarilla"
                roja = "Tarjeta Roja"
                if amarilla in tarjeta_string:
                    tarjeta = 1
                elif roja in tarjeta_string:
                    tarjeta = 2
                else:
                    tarjeta = 0

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
                entrasale = 0
                data = [game, tournament, year, count, local, minuto, name_link, numero, posicion, capitan,
                        tarjeta, entrasale]
                with open('data.csv', 'a', encoding='UTF-8') as f:
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

                    # posicion
                    posicion = str(row.find("span", class_="posicion"))
                    posicion = " ".join(posicion.split())

                    # entrasale
                    entrasale_string = str(row.find("div", class_="disp-table"))
                    entrasale_string = " ".join(entrasale_string.split())
                    entra = "Entra"
                    sale = "Sale"
                    if entra in entrasale_string:
                        entrasale = 1
                    elif sale in entrasale_string:
                        entrasale = 2
                    else:
                        entrasale = 0

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
                    capitan = 4
                    tarjeta = 4
                    data = [game, tournament, year, count, local, minuto, name_link, numero, posicion, capitan,
                            tarjeta, entrasale]
                    with open('data.csv', 'a', encoding='UTF-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)


#LOCAL
    alineaciones = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['alineacionMin'])
    local = 1
    count = 0
    for alineacion in alineaciones:
        count = count + 1
        capitan = 0
        col_xs_12 = alineacion.find_all("li", class_="col-xs-12")
        # count = 5 son los cambios.
        if count != 5:
            for col in col_xs_12:
                # minuto.
                minuto = str(col.find("div", class_="col-xs-2 minutoGol"))
                minuto = " ".join(minuto.split())

                # name
                name = str(col.find("div", class_="jugador"))
                name = " ".join(name.split())
                html = BeautifulSoup(name, 'html.parser')
                name = str([a['href'] for a in html.find_all('a')])[2:-2]
                name_link = "http://ligamx.net" + str(name)

                # numero y capitan
                numero = str(col.find("strong", class_="numero"))
                numero = " ".join(numero.split())
                fullstring = numero
                substring = "capitan"
                if substring in fullstring:
                    capitan = 1
                else:
                    capitan = 0

                # posicion
                posicion = str(col.find("span", class_="posicion"))
                posicion = " ".join(posicion.split())

                # tarjetas
                tarjeta_string = str(col.find("div", class_="disp-table"))
                tarjeta_string = " ".join(tarjeta_string.split())

                amarilla = "Tarjeta Amarilla"
                roja = "Tarjeta Roja"
                if amarilla in tarjeta_string:
                    tarjeta = 1
                elif roja in tarjeta_string:
                    tarjeta = 2
                else:
                    tarjeta = 0

                # print(tarjeta)

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

                entrasale = 0
                data = [game, tournament, year, count, local, minuto, name_link, numero, posicion, capitan,
                        tarjeta, entrasale]
                with open('data.csv', 'a', encoding='UTF-8') as f:
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
                    elif sale in entrasale_string:
                        entrasale = 2
                    else:
                        entrasale = 0

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

                    capitan = 4
                    tarjeta = 4
                    data = [game, tournament, year, count, local, minuto, name_link, numero, posicion, capitan,
                            tarjeta, entrasale]
                    with open('data.csv', 'a', encoding='UTF-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)

# Step 1: Init multiprocessing.Pool()
pool = mp.Pool(mp.cpu_count())
print(mp.cpu_count())
# Step 2: `pool.apply` the `howmany_within_range()
results = pool.starmap(funcion,[(game,) for game in csvrows])
#[pool.apply(funcion, args=(game,)) for game in csvrows]
# Step 3: Don't forget to close
pool.close()