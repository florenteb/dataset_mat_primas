from scraper_aceite import *
from api_eurostat import *


# Carga de los datos Eurostat
ref_indice_q = 'apri_pi15_outq?product=080000&filterNonGeo=1&precision=1&geo=ES&sinceTimePeriod=2015Q1&precision=2&p_adj=NI&unit=PCH_SM'
ref_precio_a_virgen_extra = 'apri_ap_crpouta?sinceTimePeriod=2015&filterNonGeo=1&precision=1&geo=ES&precision=2&prod_veg=08100000&currency=EUR'
ref_precio_a_virgen = 'apri_ap_crpouta?sinceTimePeriod=2015&filterNonGeo=1&precision=1&geo=ES&precision=2&prod_veg=08500000&currency=EUR'
ref_precio_a_lampante = 'apri_ap_crpouta?sinceTimePeriod=2015&filterNonGeo=1&precision=1&geo=ES&precision=2&prod_veg=08400000&currency=EUR'
ref_ipc_a = 'tec00118?sinceTimePeriod=2015&precision=1&filterNonGeo=1&precision=1&geo=ES&unit=RCH_A_AVG&coicop=CP00'
ref_ipc_m = 'teicp010?filterNonGeo=1&precision=1&geo=ES&unit=PCH_M1&coicop=CP01'

dfIndAgriQ = genera_dataframe_eurostat(ref_indice_q)
dfPrecAVEA = genera_dataframe_eurostat(ref_precio_a_virgen_extra)
dfPrecAVA = genera_dataframe_eurostat(ref_precio_a_virgen)
dfPrecALA = genera_dataframe_eurostat(ref_precio_a_lampante)
dfIPCA = genera_dataframe_eurostat(ref_ipc_a)
dfIPCM = genera_dataframe_eurostat(ref_ipc_m)

# Carga de los datos diarios del precio del aceite
dfAceiteDiario = genera_dataframe_aceite('01/01/2015', '31/12/2019')

# Preparación de los datos
# Precios anuales de aceite
# Juntamos los tres tipos de aceite
dfAceite = dfPrecAVEA.append(dfPrecAVA, ignore_index=True).append(dfPrecALA, ignore_index=True)
dfAceite.columns.values[2] = 'Fecha'
dfAceite["Fecha"] = ["Aceite oliva Virgen Extra Esp anual",
                     "Aceite oliva Virgen Esp anual", "Aceite oliva Lampante Esp anual"]
# Transponemos tabla: filas por años
dfAceite2 = dfAceite.transpose()
dfAceite2.columns = dfAceite["Fecha"]
# Limpiamos los primeros registros (etiquetas)
dfAceite = dfAceite2[3:]
# Convertimos a diario
dfAceite = df_anual_a_diario(dfAceite)


# Repetimos para el IPC anual
dfIPC = dfIPCA
dfIPC.columns.values[0] = 'Fecha'
dfIPC2 = dfIPCA.transpose()
dfIPC2.columns = ['IPC anual a-a']
dfIPC = dfIPC2[3:]
dfIPC_A = df_anual_a_diario(dfIPC)


# Indice Precios agrícolas trimestral
# Transponemos tabla: filas por trimestres
dfIndAgri = dfIndAgriQ
dfIndAgri.columns.values[2] = 'Fecha'
dfIndAgri2 = dfIndAgri.transpose()
dfIndAgri2.columns = ["Ind Prec Agri trimestral t-t"]
# Limpiamos los primeros registros (etiquetas)
dfIndAgri = dfIndAgri2[3:]
# Convertimos a diario
dfIndAgri = df_trimestral_a_diario(dfIndAgri)

# IPC mensual
# Transponemos tabla: filas por meses
dfIPC = dfIPCM
dfIPC.columns.values[2] = 'Fecha'
dfIPC2 = dfIPC.transpose()
dfIPC2.columns = ["IPC mensual m-m"]
# Limpiamos los primeros registros (etiquetas)
dfIPC = dfIPC2[3:]
# Convertimos a diario
dfIPC = df_mensual_a_diario(dfIPC)

# Juntamos todo en el dataset final
dfFinal = pd.merge(dfAceite, dfIPC, on='Fecha', how='outer', suffixes=['_and', '_or'])
dfFinal = pd.merge(dfFinal, dfIPC_A, on='Fecha', how='outer', suffixes=['_and', '_or'])
dfFinal = pd.merge(dfFinal, dfIndAgri, on='Fecha', how='outer', suffixes=['_and', '_or'])
# Quitamos los registros de 2020 ya que no hay datos en muchos de los datasets originales
dfFinal = dfFinal[(dfFinal.Fecha < "20200101")]

# Adaptamos el dataset del precio diario del aceite al formato del dataset final
dfAceiteDiarioP = dfAceiteDiario.groupby(['Fecha', 'Clase']).Precio.first().unstack()
# Adaptamos el formato de fecha para poder cruzar con el dataset anterior.
dfAceiteDiarioP['Fecha'] = dfAceiteDiarioP.index
dfAceiteDiarioP['Fecha'] = (dfAceiteDiarioP['Fecha'].str[6:10] +
                            dfAceiteDiarioP['Fecha'].str[3:5]+dfAceiteDiarioP['Fecha'].str[0:2])
dfAceiteDiarioP.index.names = ['Indice']
dfFinal['Fecha'] = dfFinal['Fecha']
dfFinal = pd.merge(dfFinal, dfAceiteDiarioP, on='Fecha', how='outer', suffixes=['_and', '_or'])

# Generación del fichero .csv
nombre_fichero = "Dataset_Aceite_"+str(datetime.datetime.now().timestamp())+".csv"
dfFinal.to_csv(nombre_fichero, sep=';', encoding='utf-8', index=False)
print("Fichero", nombre_fichero, "generado.")
