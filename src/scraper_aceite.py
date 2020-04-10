from bs4 import BeautifulSoup
import re
import urllib.error
from urllib.request import urlopen, Request
import urllib.parse
import time
import datetime
import pandas as pd


def __descarga_url(url, num_retries=2, file=0):
    # Método que descarga el contenido de la url pasada por parámetro url,
    # con parámetros opcionales num_retries para  el número de reintentos y
    # file para el almacenamiento del contenido en un fichero.
    print('Descargando:', url)
    try:
        request = Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        )
    except Exception:
        print("__descarga_url - error: error de página")
        html = None
    try:
        # Descarga del contenido de la URL
        html = urlopen(request).read().decode('iso-8859-1', 'replace')
        if (file == 1):
            # Almacenamos fichero en disco
            filename = (url.split("/")[-1])+"_" + \
                datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+str(time.time())+".html"
            print("Guardando página: ", filename)
            with open(filename, "w") as file:
                file.write(html)
    except urllib.error.URLError as e:
        print('__descarga_url - error: ', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # Reintento ante errores 5XX HTTP
                return __descarga_url(url, num_retries-1)
    return html


def __extrae_por_fecha(fecha_ini, fecha_fin):
    # La web que queremos "scrapear" no admite rangos de extracción de datos superiores
    # a 2 meses, por lo que hay que realizar sucesivas llamadas en caso de necesitar un
    # rango más amplio. Por seguridad, los rangos son de 4 semanas.
    # Los parámetros del método son la fecha inicial y final del rango.
    soup = []
    try:
        ini = datetime.datetime.strptime(fecha_ini, '%d/%m/%Y')
        fin = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y')
    except Exception:
        # Control del formato de fechas
        print("__extrae_por_fecha - error: fechas no válidas. Formato admitido: dd/mm/aaaa")
        return
    if (fecha_ini == fecha_fin):
        n_dias = 1
    else:
        n_dias = int(str(fin - ini).split()[0])
    if (n_dias <= 28):
        # Si el rango es menor a 4 semanas, realizamos una sola llamada.
        page_link = 'http://www.infaoliva.com/paginas/ObservatorioFechas.asp?fechaini=' + \
            datetime.datetime.strftime(ini, '%d/%m/%Y')+'&fechafin=' + \
            datetime.datetime.strftime(fin, '%d/%m/%Y')
        page = __descarga_url(page_link)
        soup.append(BeautifulSoup(page, features="html5lib"))
    else:
        # Para rangos superiores, se realizan sucesivas llamadas
        fin_for = ini
        array_pos = 0
        while (fin_for < fin):
            fin_for = ini + datetime.timedelta(days=27)
            if (fin_for >= fin):
                fin_for = fin
            page_link = 'http://www.infaoliva.com/paginas/ObservatorioFechas.asp?fechaini=' + \
                datetime.datetime.strftime(ini, '%d/%m/%Y')+'&fechafin=' + \
                datetime.datetime.strftime(fin_for, '%d/%m/%Y')
            page = __descarga_url(page_link)
            soup.append(BeautifulSoup(page, features="html5lib"))
            ini = ini + datetime.timedelta(days=28)
    return soup


def __obten_cotizaciones(soup):
    # Extracción de las cotizaciones de aceite del objeto soup creado con __extrae_por_fecha
    lista_aceite = []
    trs = soup.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if not tds:
            continue
        if (len(tds) < 3):
            continue
        lista_aceite.append(
            [tds[0].text.strip(), tds[1].text.strip(), tds[2].text.strip()])
    return lista_aceite


def __elimina_tags(text):
    # Limpieza de las cadenas de texto HTML
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def __obten_dias(soup):
    # Extracción de los días de cotizaciones del el objeto soup creado con __extrae_por_fecha
    lista_dias = []
    divs = soup.find_all("div", {"class": "pull-right"})
    for div in divs:
        dia = str.split(__elimina_tags(str(div)))
        dia = [dia[2], dia[1]]
        lista_dias.append(dia)
        lista_dias.append(dia)
        lista_dias.append(dia)
    return lista_dias


def genera_dataframe_aceite(fecha_ini, fecha_fin, genera_fichero=0):
    # Generación de un dataframe con las cotizaciones por fecha, en el rango indicado
    # entre fecha_ini y fecha_fin y con posibilidad de generar un fichero csv con el
    # parámetro genera_fichero
    soups = __extrae_por_fecha(fecha_ini, fecha_fin)
    # Almacena la extracción en un dataframe
    dfAceite = pd.DataFrame(
        columns=['Fecha', 'Día', 'Clase', 'Variedad', 'Precio'])
    for soup in soups:
        dfCot = pd.DataFrame(__obten_cotizaciones(soup), columns=[
                             'Clase', 'Variedad', 'Precio'])
        dfDia = pd.DataFrame(__obten_dias(soup), columns=['Fecha', 'Día'])
        if (len(dfCot) != len(dfDia)):
            print("ATENCIÓN: Hay inconsistencias entre los registros de aceite y de fechas. Compruebe si ha cambiado la estructura de los datos.")
        dfFor = pd.concat([dfCot, dfDia], axis=1)
        dfAceite = dfAceite.append(dfFor, ignore_index=True)
    if (genera_fichero == 1):
        # Generación del fichero .csv
        fecha_ini = fecha_ini.replace("/", "")
        fecha_fin = fecha_fin.replace("/", "")
        nombre_fichero = "Dataset_Aceite_"+fecha_ini+"_"+fecha_fin+".csv"
        dfAceite.to_csv(nombre_fichero, sep=';', encoding='utf-8', index=False)
        print("Fichero", nombre_fichero, "generado.")
    return dfAceite
