import requests
import urllib.error
from urllib.request import urlopen, Request
import pandas as pd
import datetime
import re


def genera_dataframe_eurostat(ref_dataset, genera_fichero=0):
    # Generación de un dataset utilizando la API de Eurostat, pasando
    # como referencia los parámetros de la API con ref_dataset, y posibilidad
    # de generar un fichero csv en salida con el parámetro genera_fichero.
    url = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/unicode/en/'+ref_dataset
    print('Descargando:', url)
    response = requests.get(url)
    if (response.status_code != 200):
        print("Error al obtener datos: ", response)
        return None
    datos = response.text
    # Nos quedamos sólo con la parte de datos, a partir de SLICE
    re.search('SLICE(.*)', datos).group(1)
    a = datos.find('SLICE')
    datos = (datos[a+len('SLICE'):])
    # Limpiamos los datos recibidos
    datos = datos.replace("\t", ";").replace("(:)", "NA").replace("(:,z)", "NA")
    filas = datos.split('\r\n')
    # Organizamos los datos para insertarlos en un pandas dataframe
    tabla = [n.split(';') for n in filas]
    dfEurostat = pd.DataFrame(tabla)
    dfEurostat.columns = dfEurostat.iloc[0]
    dfEurostat = dfEurostat.reindex(dfEurostat.index.drop(0))
    dfEurostat = dfEurostat.rename({'NA': 'Country'}, axis=1)
    dfEurostat = dfEurostat[:-1]
    if (genera_fichero == 1):
        # Generación del fichero .csv
        nombre_fichero = "Dataset_Eurostat_"+ref_dataset+".csv"
        dfEurostat.to_csv(nombre_fichero, sep=';', encoding='utf-8', index=False)
        print("Fichero", nombre_fichero, "generado.")
    return(dfEurostat)


def df_anual_a_diario(dfAnual):
    # Método que tomando un conjunto de datos anual, lo convierte a diario
    # asignando a cada uno de los días el valor del año al que pertenece.
    pd.set_option('mode.chained_assignment', None)
    dfAnual2 = pd.DataFrame()
    dfAnual["Fecha"] = -1
    date = datetime.datetime.strptime('01/01/'+dfAnual.index[0], '%d/%m/%Y')
    for a in (dfAnual.index.tolist()):
        dfFor = pd.DataFrame([dfAnual.loc[a]])
        if (int(a) % 4 == 0):  # si es bisiesto, añade un dia mas
            dfFor = dfFor.append([dfAnual.loc[a]]*365)
        else:
            dfFor = dfFor.append([dfAnual.loc[a]]*364)
        for i in range(0, len(dfFor)):
            datestr = datetime.datetime.strftime(date, '%Y%m%d')
            dfFor.iloc[i, dfFor.columns.get_loc('Fecha')] = datestr
            date = date + datetime.timedelta(1)
        dfAnual2 = dfAnual2.append(dfFor)
    return dfAnual2


def df_trimestral_a_diario(dfTrimestral):
    # Método que tomando un conjunto de datos trimestral, lo convierte a diario
    # asignando a cada uno de los días el valor del trimestre al que pertenece.
    pd.set_option('mode.chained_assignment', None)
    dfTrimestral2 = pd.DataFrame()
    dfTrimestral["Fecha"] = -1
    anyo = str(dfTrimestral.index[0])[0:4]
    # Extraemos el mes inicial
    if (str(dfTrimestral.index[0])[4:6] == "Q1"):
        mes = "01"
    elif (str(dfTrimestral.index[0])[4:6] == "Q2"):
        mes = "04"
    elif (str(dfTrimestral.index[0])[4:6] == "Q3"):
        mes = "07"
    else:
        mes = "10"

    date = datetime.datetime.strptime('01/'+mes+'/'+anyo, '%d/%m/%Y')
    for a in (dfTrimestral.index.tolist()):
        dfFor = pd.DataFrame([dfTrimestral.loc[a]])
        # En función de si el año es bisiesto, y del trimestre, creamos el número
        # de días adecuado.
        if (a[4:6] == 'Q1'):
            if (int(a[0:4]) % 4 == 0):
                dfFor = dfFor.append([dfTrimestral.loc[a]]*90)
            else:
                dfFor = dfFor.append([dfTrimestral.loc[a]]*89)

        elif (a[4:6] == 'Q2'):
            dfFor = dfFor.append([dfTrimestral.loc[a]]*90)
        else:
            dfFor = dfFor.append([dfTrimestral.loc[a]]*91)
        for i in range(0, len(dfFor)):
            datestr = datetime.datetime.strftime(date, '%Y%m%d')
            dfFor.iloc[i, dfFor.columns.get_loc('Fecha')] = datestr
            date = date + datetime.timedelta(1)
        dfTrimestral2 = dfTrimestral2.append(dfFor)
    return dfTrimestral2


def df_mensual_a_diario(dfMensual):
    # Método que tomando un conjunto de datos mensual, lo convierte a diario
    # asignando a cada uno de los días el valor del mes al que pertenece.
    pd.set_option('mode.chained_assignment', None)
    dfMensual2 = pd.DataFrame()
    dfMensual["Fecha"] = -1
    anyo = str(dfMensual.index[0])[0:4]
    mes = str(dfMensual.index[0])[5:7]

    date = datetime.datetime.strptime('01/'+mes+'/'+anyo, '%d/%m/%Y')

    for a in (dfMensual.index.tolist()):
        dfFor = pd.DataFrame([dfMensual.loc[a]])
        # En función de si el año es bisiesto, y del mes, creamos el número
        # de días adecuado.
        if (a[4:7] == 'M02'):
            if (int(a[0:4]) % 4 == 0):
                dfFor = dfFor.append([dfMensual.loc[a]]*28)
            else:
                dfFor = dfFor.append([dfMensual.loc[a]]*27)

        elif (a[4:7] == 'M04' or a[4:7] == 'M06' or a[4:7] == 'M09' or a[4:7] == 'M11'):
            dfFor = dfFor.append([dfMensual.loc[a]]*29)
        else:
            dfFor = dfFor.append([dfMensual.loc[a]]*30)
        for i in range(0, len(dfFor)):
            datestr = datetime.datetime.strftime(date, '%Y%m%d')
            dfFor.iloc[i, dfFor.columns.get_loc('Fecha')] = datestr
            date = date + datetime.timedelta(1)
        dfMensual2 = dfMensual2.append(dfFor)
    return dfMensual2
