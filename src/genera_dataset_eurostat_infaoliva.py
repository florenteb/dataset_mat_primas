from scraper_aceite import genera_dataframe_aceite
from api_eurostat import genera_dataframe_eurostat
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Carga de los datos Eurostat (parámetros de la llamada)
ref_indice_q = 'apri_pi15_outq?product=080000&filterNonGeo=1&precision=1&geo=ES&sinceTimePeriod=2017Q1&precision=2&p_adj=NI&unit=PCH_SM'
ref_ipc_a = 'tec00118?sinceTimePeriod=2017&precision=1&filterNonGeo=1&precision=1&geo=ES&unit=RCH_A_AVG&coicop=CP00'
ref_ipc_m = 'teicp010?filterNonGeo=1&precision=1&geo=ES&unit=PCH_M1&coicop=CP01'
# Carga de los datos de Eurostat (llamada)
dfIndAgriQ = genera_dataframe_eurostat(ref_indice_q)
dfIPCA = genera_dataframe_eurostat(ref_ipc_a)
dfIPCM = genera_dataframe_eurostat(ref_ipc_m)
# Carga de los datos diarios del precio del aceite (infaoliva)
dfAceiteDiario = genera_dataframe_aceite('01/01/2017', '31/12/2019')


# Genera dfAceite mensual con los datos de infaoliva diarios
dfAceiteMensual = dfAceiteDiario.copy()
# Limpiamos los registros sin cotización
dfAceiteMensual = dfAceiteMensual[dfAceiteMensual.Precio != "Sin cotización"]
dfAceiteMensual = dfAceiteMensual.reset_index(drop=True)
dfAceiteMensual["Año"] = -1
dfAceiteMensual["Mes"] = -1
# Convertimos al formato del resto de datasets
for i in range(len(dfAceiteMensual)):
    dfAceiteMensual["Año"][i] = int(dfAceiteMensual["Fecha"][i][6:10])
    dfAceiteMensual["Mes"][i] = int(dfAceiteMensual["Fecha"][i][3:5])
    dfAceiteMensual.Precio[i] = float(
        dfAceiteMensual.Precio[i][:-2].replace(',', '.'))
dfAceite = pd.DataFrame(columns=["Producto", "Precio", "Año", "Mes", "Origen"])
# Convertimos los datos en mensuales con la media de precios de cada mes
for a in np.unique(dfAceiteMensual.Año):
    for m in np.unique(dfAceiteMensual.Mes[dfAceiteMensual.Año == a]):
        for p in np.unique(dfAceiteMensual.Clase[(dfAceiteMensual.Mes == m) & (dfAceiteMensual.Año == a)]):
            precio = dfAceiteMensual.Precio[(dfAceiteMensual.Clase == p) & (
                dfAceiteMensual.Mes == m) & (dfAceiteMensual.Año == a)].mean()
            dfAceite = dfAceite.append(
                {'Producto': p, 'Precio': precio, 'Año': a, 'Mes': m,
                 'Origen': "Infaoliva"}, ignore_index=True)


# Genera dfIPCMensual con los datos del IPC mes a mes
dfIPC = dfIPCM
dfIPC.columns.values[2] = 'Fecha'
dfIPC = dfIPC.transpose()
dfIPC.columns = ["IPC mensual m-m"]
# Limpiamos los primeros registros (etiquetas)
dfIPC = dfIPC[3:]
dfIPCMensual = pd.DataFrame(
    columns=["Producto", "Precio", "Año", "Mes", "Origen"])
# Almacenamos los valores en el formato del resto de datasets
for i in range(len(dfIPC)):
    dfIPCMensual = dfIPCMensual.append(
        {'Producto': 'IPC mensual mes a mes',
         'Precio': dfIPC.iloc[i][0],
         'Año': dfIPC.iloc[i].name[0:4],
         'Mes': dfIPC.iloc[i].name[5:7],
         'Origen': "Eurostat"}, ignore_index=True)


# Genera dfIPCAnual con los datos del IPC anuales convertidos en mensual
dfIPC = dfIPCA
dfIPC.columns.values[0] = 'Fecha'
dfIPC = dfIPCA.transpose()
dfIPC.columns = ['IPC anual a-a']
# Limpiamos los primeros registros (etiquetas)
dfIPC = dfIPC[3:]
dfIPCAnual = pd.DataFrame(
    columns=["Producto", "Precio", "Año", "Mes", "Origen"])
# Almacenamos los valores en el formato del resto de datasets
for i in range(len(dfIPC)):
    for m in range(12):
        dfIPCAnual = dfIPCAnual.append(
            {'Producto': 'IPC anual año a año',
             'Precio': dfIPC.iloc[i][0],
             'Año': dfIPC.iloc[i].name,
             'Mes': m+1, 'Origen': "Eurostat"},
            ignore_index=True)


# Genera dfIndAgricola con los datos del IP agrícola trimestral trimestre a trimestre
dfIndAgri = dfIndAgriQ
dfIndAgri.columns.values[2] = 'Fecha'
dfIndAgri = dfIndAgri.transpose()
dfIndAgri.columns = ["Ind Prec Agri trimestral t-t"]
# Limpiamos los primeros registros (etiquetas)
dfIndAgri = dfIndAgri[3:]
dfIndAgricola = pd.DataFrame(
    columns=["Producto", "Precio", "Año", "Mes", "Origen"])
# Almacenamos los valores en el formato del resto de datasets: convertimos datos trimestrales
# a mensuales
for i in range(len(dfIndAgri)):
    meses = {}
    if(dfIndAgri.iloc[i].name[4:7] == 'Q1'):
        meses = {1, 2, 3}
    elif(dfIndAgri.iloc[i].name[4:7] == 'Q2'):
        meses = {4, 5, 6}
    elif(dfIndAgri.iloc[i].name[4:7] == 'Q3'):
        meses = {7, 8, 9}
    elif(dfIndAgri.iloc[i].name[4:7] == 'Q4'):
        meses = {10, 11, 12}
    for m in meses:
        dfIndAgricola = dfIndAgricola.append(
            {'Producto': 'Ind. prec. agrícolas trimestre a trimestre',
             'Precio': dfIndAgri.iloc[i][0],
             'Año': dfIndAgri.iloc[i].name[0:4],
             'Mes': m, 'Origen': "Eurostat"},
            ignore_index=True)


# Agrupamos los datasets en dfFinal
dfFinal = dfIPCMensual.append(dfIPCAnual, ignore_index=True).append(
    dfIndAgricola, ignore_index=True).append(dfAceite, ignore_index=True)
dfFinal = dfFinal[dfFinal.Año != '2020']
dfFinal.index.name = "index"


# Generación del fichero .csv
nombre_fichero = "Dataset_Infaoliva_Eurostat" + \
    '_20170101_20191231.csv'
dfFinal.to_csv(nombre_fichero, sep=';', encoding='utf-8', index=True)
print("Fichero", nombre_fichero, "generado.")
