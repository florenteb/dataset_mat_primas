from bs4 import BeautifulSoup
import re
import collections
import itertools
import requests
import urllib.error
from urllib.request import urlopen, Request
import urllib.parse
import queue
import time
import datetime
import pandas as pd

def descarga_url(url, num_retries=2, file=0):
    print('Descargando:', url)
    try:
        request = Request(
        url,
        data=None,
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        )
    except Exception:
        print ("descarga_url - error: error de página")
        html=None
    try:
        html = urlopen(request).read().decode('iso-8859-1', 'replace')
        filename = (url.split("/")[-1])+"_"+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+str(time.time())+".html"
        if (file==1):
            print("Guardando página: ",filename)
            with open(filename, "w") as file:
                file.write(html)
    except urllib.error.URLError as e:
        print('descarga_url - error: ', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # reintento ante errores 5XX HTTP
                return descarga_url(url, num_retries-1)
    return html

# extrae por fechas
def extrae_por_fecha (fecha_ini, fecha_fin):
    soup = []
    try:
        ini = datetime.datetime.strptime(fecha_ini, '%d/%m/%Y')
        fin = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y')
    except Exception:
        print ("extrae_por_fecha - error: fechas no válidas. Formato admitido: dd/mm/aaaa")
        return
    if (fecha_ini == fecha_fin):
        n_dias = 1
    else:
        n_dias = int(str(fin - ini).split()[0])
    if (n_dias <= 28):
        page_link = 'http://www.infaoliva.com/paginas/ObservatorioFechas.asp?fechaini='+datetime.datetime.strftime(ini,'%d/%m/%Y')+'&fechafin='+datetime.datetime.strftime(fin,'%d/%m/%Y')
        page = descarga_url(page_link)
        soup.append(BeautifulSoup(page,features="html5lib"))
    else:
        fin_for = ini
        array_pos = 0
        while (fin_for < fin):
            fin_for = ini + datetime.timedelta(days=27)
            if (fin_for >= fin):
                fin_for = fin
            page_link = 'http://www.infaoliva.com/paginas/ObservatorioFechas.asp?fechaini='+datetime.datetime.strftime(ini,'%d/%m/%Y')+'&fechafin='+datetime.datetime.strftime(fin_for,'%d/%m/%Y')
            page = descarga_url(page_link)
            soup.append(BeautifulSoup(page,features="html5lib"))
            ini = ini + datetime.timedelta(days=28)
    return soup

# Obten cotizaciones
def obten_cotizaciones(soup):
    lista_aceite = []
    trs = soup.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if not tds: continue
        if (len(tds)<3): continue
        lista_aceite.append([tds[0].text.strip(), tds[1].text.strip(), tds[2].text.strip()])
    return lista_aceite

    # metodo para eliminar tags
def elimina_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

# Obten días
def obten_dias(soup):
    lista_dias = []
    divs = soup.find_all("div", {"class": "pull-right"})
    for div in divs:
        dia = str.split(elimina_tags(str(div)))
        dia = [dia[2],dia[1]]
        lista_dias.append(dia)
        lista_dias.append(dia)
        lista_dias.append(dia)
    return lista_dias

def genera_dataframe_aceite(fecha_ini, fecha_fin, genera_fichero=0):
    soups = extrae_por_fecha(fecha_ini,fecha_fin)
    # Almacena la extracción en un dataframe
    dfAceite = pd.DataFrame(columns = ['Fecha' , 'Día', 'Clase' , 'Variedad', 'Precio'])
    for soup in soups:
        dfCot = pd.DataFrame(obten_cotizaciones(soup), columns = ['Clase' , 'Variedad', 'Precio'])
        dfDia = pd.DataFrame(obten_dias(soup),columns = ['Fecha' , 'Día'])
        if (len(dfCot)!=len(dfDia)):
            print("ATENCIÓN: Hay inconsistencias entre los registros de aceite y de fechas. Compruebe si ha cambiado la estructura de los datos.")
        dfFor = pd.concat([dfCot, dfDia], axis=1)
        dfAceite = dfAceite.append(dfFor, ignore_index=True)
    if (genera_fichero==1):
        fecha_ini = fecha_ini.replace("/","")
        fecha_fin = fecha_fin.replace("/","")
        nombre_fichero = "Dataset_Aceite_"+fecha_ini+"_"+fecha_fin+".csv"
        dfAceite.to_csv(nombre_fichero, sep=';', encoding='utf-8', index=False)
        print("Fichero",nombre_fichero,"generado.")
    return dfAceite

genera_dataframe_aceite("01/07/2019","01/01/2020",1)
