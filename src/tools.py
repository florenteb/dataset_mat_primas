from dateutil.parser import parse
import datetime as dt

def Extract_Year_from_date(fecha):
    if isinstance(fecha, str): fecha = parse(fecha)
    return (fecha.year)

def Extract_Month_from_date(fecha):
    if isinstance(fecha, str): fecha = parse(fecha)
    return (fecha.month)

def last_day_Month(fecha):

    if isinstance(fecha, str): fecha = parse(fecha)
         
    año = Extract_Year_from_date(fecha)
    mes = Extract_Month_from_date(fecha)
    ahora = dt.datetime.now().date()
    if (mes<12):
        last_day_of_month = (parse(str(año)+'-'+ str(mes+1) + '-' + '01') - dt.timedelta(days=1)).date()
    else:
        last_day_of_month = (parse(str(año)+'-'+ '12-31')).date()

    if (last_day_of_month >= ahora):
        return(ahora)
    else:     
        return(last_day_of_month)

def Save_df_to_csv(df, name, fecha_ini, fecha_fin):
    # Generación del fichero .csv
        fecha_ini = fecha_ini.replace("/", "")
        fecha_ini = fecha_ini.replace("-", "")
        fecha_fin = fecha_fin.replace("/", "")
        fecha_fin = fecha_fin.replace("-", "")
        nombre_fichero = name + "_" + fecha_ini + "_" + fecha_fin + ".csv"
        df.to_csv(nombre_fichero, sep=';', encoding='utf-8', index=False)
        print("Fichero", nombre_fichero, "generado.")
        return(nombre_fichero)