from tools import *
from Scraping_MercaAlicante import *
from Scraping_MercaMadrid import *
import datetime as dt

def date_vector(año_inicio, año_fin, mes_inicio, mes_final, dia):
    # It generates a date vector with dates.
    # Output: a vector of strings 
    fecha=[]
    for año in range(año_inicio, año_fin +1):
        for mes in range(mes_inicio,mes_final +1):
            fecha.append(str(dt.date(año, mes, dia)))
    return(fecha)
    

# Main program    
if '__main__' == __name__:
    # Date Extraction from MercAlicante
    
    fecha_inicio = date_vector(2017, 2019, 1, 12, 1)
        
    if 1==0:
        print('MercAlicante Data Extractor')
        print('--------------------------')
        producto='' #Void all products
        familia='' # Void all families
        categoria = '106' # Frutas 
        pos=1
        for fecha in fecha_inicio:
            # Calculate the last day of the month or current day
            fecha_Fin = str(last_day_Month(fecha))
            df = Scraping_MercAlicante(producto, familia, 
                categoria, fecha, fecha_Fin)
            df_Mercalicante=df if pos==1 else pd.concat([df_Mercalicante, df])
            pos +=1
            
        Save_df_to_csv(df_Mercalicante,'MercAlicante',fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
    if 1==0:    
        # Date Extraction from MercaMadrid
        print('')
        print('MercaMadrid Data Extractor')
        print('--------------------------')
        browser = 'Chrome'
        pos=1
        for fecha in fecha_inicio:

            fecha_fin = str(last_day_Month(fecha))
            df= Scraping_MercaMardrid(browser,'MERCADO CENTRAL DE FRUTAS', fecha, fecha_fin)
            df_MercaMadrid = df if pos==1 else pd.concat([df_MercaMadrid, df])
            pos +=1
        Save_df_to_csv(df_MercaMadrid,'MercaMadrid',fecha_inicio[0], str(last_day_Month(fecha_inicio[-1])))
    
    # Unificando datasets
    #columns = ['Año', 'Mes', 'Origen','Producto', 'Precio']
    
    if 1==0:
        # MercAlicante
        df1= pd.read_csv('MercAlicante_20190101_20191231.csv', sep=';')
        df2= pd.read_csv('MercAlicante_20180101_20181231.csv', sep=';')
        df3= pd.read_csv('MercAlicante_20170101_20171231.csv', sep=';')
        print('Datasets MercaMadrid loaded')
        print('Size: ', len(df1), len(df2), len(df3))
        df1 = pd.concat([df1.reset_index(), df2.reset_index()], ignore_index=True)
        df1 = pd.concat([df1.reset_index(), df3.reset_index()], ignore_index=True)
        columns = ['Producto','Frecuente','Año','Mes','Origen']
        df1 = df1[columns] # Select the columns
        df1.rename(columns={'Frecuente' : 'Precio'}, inplace= True) 
        Save_df_to_csv(df1,'MercAlicante','2017-01-01', '2019-12-31')
        print('Total rows: ', len(df1))
    if 1==0:
        # MercaMadrid
        df1= pd.read_csv('MercaMadrid_20190101_20191231.csv', sep=';')
        df2= pd.read_csv('MercaMadrid_20180101_20181231.csv', sep=';')
        df3= pd.read_csv('MercaMadrid_20170101_20171231.csv', sep=';')
        print('Datasets MercaMadrid loaded')
        print( 'Size: ', len(df1), len(df2), len(df3))
        df1 = pd.concat([df1.reset_index(), df2.reset_index()], ignore_index=True)
        df1 = pd.concat([df1.reset_index(), df3.reset_index()], ignore_index=True)
        # Algunos registros no tienen informado el campo Producto, pero sí el campo Variedad
        
        columns = ['Variedad','Precio frecuente','Año','Mes','Origen']
        df1 = df1[columns]
        df1.rename(columns={'Precio frecuente' : 'Precio', 'Variedad':'Producto'}, inplace= True)
        Save_df_to_csv(df1,'MercaMadrid','2017-01-01', '2019-12-31')
        print('Total rows: ', len(df1))

    if 1==0:
        # Unificación MercAlicante y MercaMadrid
        df1= pd.read_csv('MercAlicante_20170101_20191231.csv', sep=';')
        df2= pd.read_csv('MercaMadrid_20170101_20191231.csv', sep=';')
        print('MercAlicante and MercaMadrid Union ')
        print( 'Size: ', len(df1), len(df2))
        df1 = pd.concat([df1.reset_index(), df2.reset_index()], ignore_index=True)
        print('Total rows: ', len(df1))
        Save_df_to_csv(df1,'Mercados Centrales','2017-01-01', '2019-12-31')